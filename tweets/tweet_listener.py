import tweepy
import json
from django.conf import settings
from tweets.models import Tweet, User


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
