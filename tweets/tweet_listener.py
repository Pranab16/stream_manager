import tweepy
import json

from tweets.models import Tweet, User


# This class is used to create tweets and users
# It is used as a listener for real-time streaming
class TweetListener(tweepy.StreamListener):
    def on_data(self, data):
        try:
            data = json.loads(data)

            # check if user with screen name exists else create a new user
            user, created = User.objects.get_or_create(screen_name=data['user']['screen_name'],
                defaults={'name': data['user']['name']}
            )
            # Create a new tweet
            tweet = Tweet(text=data['text'], tweet_id=data['id_str'], user_id=user)
            tweet.save()
        except Exception, e:
            print e

        return True
