from swampdragon.serializers.model_serializer import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = 'tweets.User'
        publish_fields = ['screen_name']

class TweetSerializer(ModelSerializer):
    class Meta:
        model = 'tweets.tweet'
        publish_fields = ['text']
