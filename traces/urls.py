from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('traces.views',
    url(r'^$', 'trace_list', name='traces'),
    url(r'^index/$', 'index', name='trace-index'),
    url(r'^record/$', 'start_record', name='start-record'),
    url(r'^(?P<trace_uuid>[a-zA-Z0-9_.-]+)$', 'trace_object',  name='trace-object'),
)
