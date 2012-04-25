from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from traces.models import Trace
from annoying.decorators import render_to

from checkins.views import get_location
 
@render_to('traces/trace_object.html')
def trace_object(request, trace_uuid):
    trace = get_object_or_404(Trace, uuid=trace_uuid)
    center = get_location(request)

    db = Trace.mongo_objects.db
    traces_mongo = db.find_one(dict(uuid=trace.uuid))
    if request.method == 'PUT':
        trace_dict = json.loads(request.raw_post_data)
        if not traces_mongo:
            traces_mongo = dict(uuid=trace.uuid, points=[])
            db.insert(traces_mongo)
        traces_mongo['points'].extend(trace_dict['points'])
        db.save(traces_mongo)
        return HttpResponse('ok')

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
        kwargs = dict(user=request.user.user)
    else:
        kwargs = {}
    trace = Trace.objects.create(**kwargs)
    if not is_authenticated:
        traces = request.session.get('traces', [])
        traces.append(trace.uuid)
        request.session['traces'] = traces
    Trace.mongo_objects.db.insert(dict(uuid=trace.uuid, points=[]))
    return redirect(trace_object, trace_uuid=trace.uuid)
    
