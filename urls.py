from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^instagram/', include('instagr.urls')),
    (r'^twitter/', include('twitter.urls')),
    (r'^traces/', include('traces.urls')),
    (r'checkins/', include('checkins.urls')),
    url(r'^facebook/login$', 'facebook.views.login', name='facebook-login'),
    url(r'^facebook/authentication_callback$', 'facebook.views.authentication_callback', name='facebook-callback'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),    
    (r'^$', 'traces.views.index'),
)

if settings.TEMPLATE_DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
