import json
import tweepy
from django.conf import settings
from tweets.models import Account


class LoadAccount():
    def __init__(self):
        pass

    def run(self):
        with open('accounts.json') as data_file:
            data = json.load(data_file)

        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        for category, accounts in data.iteritems():
            for account in accounts:
                user = api.get_user(screen_name=account['screen_name'])

                Account.objects.create(category=category, name=account['name'],
                    screen_name=account['screen_name'], id_str=user.id_str
                )
