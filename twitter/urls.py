from django.conf.urls.defaults import *

urlpatterns = patterns('twitter.views',
    url(r'^tweets/$', 'tweets',  name='tweets'),
)
