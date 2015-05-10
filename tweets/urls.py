from django.conf.urls import patterns, url

from tweets import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^start_stream/$', views.ajax_start_stream, name='ajax_start_stream'),
)
