from django.conf.urls.defaults import *

urlpatterns = patterns('instagr.views',
    url(r'^photos/$', 'photos',  name='photos'),
)
