from swampdragon import route_handler
from swampdragon.route_handler import ModelPubRouter

from django.db.models import Count

from tweets.models import Tweet, User
from tweets.serializers import TweetSerializer, UserSerializer


class UserRouter(ModelPubRouter):
    route_name = 'users'
    valid_verbs = ['subscribe', 'get_screen_name']
    model = User
    serializer_class = UserSerializer

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()

    def get_screen_name(self, **kwargs):
        users = self.model.objects.values('screen_name').annotate(count=Count('tweet'))
        max = 0
        screen_name = ''
        for user in users:
            if user['count'] > max:
                max = user['count']
                screen_name = user['screen_name']
        self.send({'screen_name': screen_name})


class TweetRouter(ModelPubRouter):
    route_name = 'tweets'
    model = Tweet
    serializer_class = TweetSerializer

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()

route_handler.register(UserRouter)
route_handler.register(TweetRouter)
