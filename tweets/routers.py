from swampdragon import route_handler
from swampdragon.route_handler import ModelPubRouter

from django.db.models import Count

from tweets.models import Tweet, User
from tweets.serializers import TweetSerializer, UserSerializer


class UserRouter(ModelPubRouter):
    route_name = 'users'
    valid_verbs = ['subscribe', 'get_count', 'get_screen_name']
    model = User
    serializer_class = UserSerializer

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()

    def get_count(self, **kwargs):
        self.send({'user_count': self.model.objects.filter(tweet__hashtag=kwargs['hashtag']).distinct('screen_name').count()})

    def get_screen_name(self, **kwargs):
        # Get tweets count for each user
        users = self.model.objects.values('screen_name').filter(tweet__hashtag=kwargs['hashtag']).annotate(count=Count('tweet'))
        max = 0
        screen_name = ''
        # get screen name of user having maximum tweet count
        for user in users:
            if user['count'] > max:
                max = user['count']
                screen_name = user['screen_name']
        self.send({'screen_name': screen_name})


class TweetRouter(ModelPubRouter):
    valid_verbs = ['subscribe', 'get_count']
    route_name = 'tweets'
    model = Tweet
    serializer_class = TweetSerializer

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()

    def get_count(self, **kwargs):
        self.send({'tweet_count': self.model.objects.filter(hashtag=kwargs['hashtag']).count()})

route_handler.register(UserRouter)
route_handler.register(TweetRouter)
