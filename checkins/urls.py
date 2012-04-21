from django.conf.urls.defaults import *
from checkins.feeds import CheckinsFeed
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', 'checkins.views.homepage', name='homepage'),
    url(r'^checkin/$', 'checkins.views.locate',  name='checkin'),
    url(r'^kml/$', CheckinsFeed(),  name='kml'),
    url(r'^checkins/$', 'checkins.views.checkins',  name='checkins'),
    url(r'^checkins/(?P<checkin_id>[a-zA-Z0-9_.-]+)/$', 'checkins.views.checkins',  name='get-checkin'),
    #url(r'^(?P<username>[a-zA-Z0-9_.-]+)/$', 'checkins.views.user_feed',  name='user-feed'),
    url(r'^(?P<country_slug>[a-zA-Z0-9_.-]+)/(?P<city_slug>[a-zA-Z0-9_.-]+)/$', 'checkins.views.homepage',  name='city'),
)
