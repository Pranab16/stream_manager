import threading
import tweepy

from django.shortcuts import render
from django.conf import settings
from django.db.models import Count
from django.conf import settings

from tweets.tweet_listener import TweetListener
from tweets.models import Tweet, User


def index(request):
    # Create a new thread to fetch tweets in real-time
    thread = threading.Thread(target=fetch_tweet)
    thread.start()

    tweets_count = Tweet.objects.all().count()
    users_count = User.objects.all().count()
    # Get count of tweets for each user
    users = User.objects.values('screen_name').annotate(count=Count('tweet'))
    max = 0
    screen_name = ''
    # get screen name of user having maximum tweet count
    for user in users:
        if user['count'] > max:
            max = user['count']
            screen_name = user['screen_name']
    context = {'tweets_count': tweets_count, 'users_count': users_count, 'screen_name': screen_name}

    return render(request, 'index.html', context)


def fetch_tweet():
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

    # fetch tweets using real-time streaming
    stream = tweepy.Stream(auth, TweetListener())
    stream.filter(track=['programming'])
