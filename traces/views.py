from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from traces.models import Trace
from annoying.decorators import render_to
from datetime import datetime
from checkins.views import get_location, MongoJSONEncoder

def get_traces(request):
    if request.user.is_authenticated():
        return Trace.objects.filter(user=request.user).order_by('-created')
    elif 'traces' in request.session:
        return Trace.objects.filter(uuid__in=request.session['traces']).order_by('-created')
    return Trace.objects.none()


@render_to('traces/index.html')
def index(request):
    center = get_location(request)
    traces = get_traces(request)
    return locals()
    
    
@render_to('traces/trace_object.html')
def trace_object(request, trace_uuid):
    trace = get_object_or_404(Trace, uuid=trace_uuid)
    center = get_location(request)
    fire_start = 'fire_start' in request.GET
    db = Trace.mongo_objects.db
    traces_mongo = db.find_one(dict(uuid=trace.uuid))
    if request.method == 'PUT':
        trace_dict = json.loads(request.raw_post_data)
        if not traces_mongo:
            traces_mongo = dict(uuid=trace.uuid, points=[])
            db.insert(traces_mongo)
        if 'points' in trace_dict:
            traces_mongo['points'].extend(trace_dict['points'])
            if not trace.title:
                addresses = filter(lambda x: x.get('formatted_address', None), traces_mongo['points'])
                if addresses:
                    trace.where_start = addresses[0]['formatted_address']
                    trace.title = '%s ~ %s' % (trace.where_start, 
                                               trace.created.strftime('%a %b %d, %X'))
                    trace.save()
                    trace.save()

            db.save(traces_mongo)
        return HttpResponse(json.dumps(traces_mongo, cls=MongoJSONEncoder))

    traces = get_traces(request).exclude(pk=trace.pk)
    points = traces_mongo and traces_mongo['points'] or []
    points = json.dumps(points)
    return locals()


@render_to('traces/trace_list.html')
def trace_list(request):
    """ Users's trace list """
    print 'trace_list', request.POST
    is_authenticated = request.user.is_authenticated()
    if is_authenticated:
        traces = Trace.objects.filter(user=request.user)
    else:
        traces = Trace.objects.filter(uuid__in=[uuid for uuid in request.session.get('traces', [])])
    return locals()


def start_record(request):
    is_authenticated = request.user.is_authenticated()
    if is_authenticated:
        kwargs = dict(user=request.user)
    else:
        kwargs = {}
    trace = Trace.objects.create(**kwargs)
    if not is_authenticated:
        traces = request.session.get('traces', [])
        traces.append(trace.uuid)
        request.session['traces'] = traces
    Trace.mongo_objects.db.insert(dict(uuid=trace.uuid, points=[]))
    return HttpResponseRedirect(reverse('trace-object', args=[trace.uuid]) + '?fire_start')
    
