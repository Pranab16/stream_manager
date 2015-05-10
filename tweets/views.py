from django.shortcuts import render
from django.http.response import HttpResponse

from tweets.tweet_listener import TweetStream


def index(request):
    context = {'tweets_count': 0, 'users_count': 0, 'screen_name': ''}
    return render(request, 'index.html', context)


# Start real-time tracking for the passed hashtag
def ajax_start_stream(request):
    hashtag = request.POST.get('hashtag')
    stream = TweetStream()
    stream.start_stream(hashtag)

    return HttpResponse(True)
