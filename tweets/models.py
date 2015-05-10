from django.db import models
from swampdragon.models import SelfPublishModel
from tweets.serializers import UserSerializer, TweetSerializer


class User(SelfPublishModel, models.Model):
    serializer_class = UserSerializer
    screen_name = models.CharField(max_length=50, blank=False, null=True)
    name = models.CharField(max_length=50, blank=False, null=True)


class Tweet(SelfPublishModel, models.Model):
    serializer_class = TweetSerializer
    text = models.TextField(max_length=500, blank=False, null=True)
    user_id = models.ForeignKey(User)
    hashtag = models.CharField(max_length=50, blank=False, null=True)
    tweet_id = models.CharField(max_length=50, blank=False, null=True)
