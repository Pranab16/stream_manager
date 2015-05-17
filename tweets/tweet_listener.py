import tweepy
import json
import threading
from django.conf import settings
from tweets.models import Tweet, User, Account, TweetMention, TweetResponse
from datetime import datetime, timedelta
from django.utils import timezone


# This class is used to create tweets and users
# It is used as a listener for real-time streaming
class TweetListener(tweepy.StreamListener):
    def __init__(self, hashtag):
        self.hashtag = hashtag
        tweepy.StreamListener.__init__(self)

    def on_data(self, data):
        try:
            data = json.loads(data)

            # check if user with screen name exists else create a new user
            user, created = User.objects.get_or_create(screen_name=data['user']['screen_name'],
                defaults={'name': data['user']['name']}
            )
            # Create a new tweet
            Tweet.objects.get_or_create(tweet_id=data['id_str'],
                defaults={'text': data['text'], 'user_id': user, 'hashtag': self.hashtag}
            )
        except Exception, e:
            print e

        return True


class MentionStreamListener(tweepy.StreamListener):
    def __init__(self):
        tweepy.StreamListener.__init__(self)

    def on_data(self, data):
        try:
            data = json.loads(data)

            account = Account.objects.filter(screen_name=data['user_mentions']['screen_name']).first

            # check if user with screen name exists else create a new user
            TweetMention.objects.get_or_create(id_str=data['id_str'],
                defaults={'account': account, 'user_id_str': data['user']['id_str'],
                          'retweeted': data['retweeted'], 'created_at': data['created_at']}
            )
        except Exception, e:
            print e

        return True


class ResponseStreamListener(tweepy.StreamListener):
    def __init__(self):
        tweepy.StreamListener.__init__(self)

    def on_data(self, data):
        try:
            data = json.loads(data)

            account = Account.objects.filter(screen_name=data['user_mentions']['screen_name']).first

            TweetResponse.objects.get_or_create(id_str=data['id_str'],
                defaults={'account': account, 'reply_id_str': data['in_reply_to_status_id_str'],
                          'created_at': data['created_at']}
            )
        except Exception, e:
            print e

        return True


class TweetStream():
    auth = None
    stream = None

    def __init__(self):
        pass

    @classmethod
    def get_auth(cls):
        if cls.auth is None:
            cls.auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
            cls.auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

    @classmethod
    def start_stream(cls, hashtag):
        cls.stop_stream()
        cls.stream = tweepy.Stream(cls.auth, TweetListener(hashtag))
        # fetch tweets using real-time streaming async
        cls.stream.filter(track=[hashtag], async=True)

    @classmethod
    def stop_stream(cls):
        if cls.stream is not None and cls.stream.running:
            cls.stream.disconnect()

    def start_mention_stream(self):
        stream = tweepy.Stream(self.auth, MentionStreamListener())
        screen_names = Account.objects.distinct('screen_name').values_list('screen_name', flat=True)
        stream.filter(track=screen_names, async=True)

    def start_response_stream(self):
        stream = tweepy.Stream(self.auth, ResponseStreamListener())
        users = Account.objects.distinct('id_str').values_list('id_str', flat=True)
        stream.filter(follow=users, async=True)

    def get_old_tweets(self):
        api = tweepy.API(self.auth)
        accounts = Account.objects.all().reverse()
        fetch_till = datetime.now() - timedelta(1)
        count = 0
        for account in accounts:
            # thr1 = threading.Thread(target=self.fetch_mentions, args=(api, account, fetch_till, count))
            # thr1.start()
            # self.fetch_mentions(api, account, fetch_till, count)
            # thr2 = threading.Thread(target=self.fetch_responses, args=(api, account, fetch_till))
            # thr2.start()
            self.fetch_responses(api, account, fetch_till)

    def fetch_mentions(self, api, account, fetch_till, count):
        count += 1
        print count
        mentions = api.search(q=account.screen_name, count=100)
        mention_data = list(mentions)
        for mention in mention_data:
            oldest_date = mention.created_at
            if oldest_date > fetch_till:
                TweetMention.objects.create(account=account, id_str=mention.id_str,
                    user_id_str=mention.user.id_str,
                    retweeted=mention.retweeted, created_at=mention.created_at)

        print oldest_date
        if oldest_date and oldest_date > fetch_till:
            self.fetch_mentions(api, account, fetch_till, count)

    def fetch_responses(self, api, account, fetch_till):
        print '*'*100
        print account.screen_name
        responses = api.user_timeline(screen_name=account.screen_name, count=100)
        response_data = list(responses)
        print len(response_data)
        print '*'*100
        for response in response_data:
            oldest_date = response.created_at
            if oldest_date > fetch_till:
                TweetResponse.objects.create(account=account, id_str=response.id_str,
                    reply_id_str=response.in_reply_to_status_id_str,
                    created_at=response.created_at)

        if oldest_date and oldest_date > fetch_till:
            self.fetch_responses(api, account, fetch_till)

