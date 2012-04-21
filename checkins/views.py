from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.template import defaultfilters
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

import pymongo
import pytz
from pymongo.objectid import ObjectId
from checkins.models import get_checkins_db, get_checkins
from checkins.forms import LocationForm 
from checkins import geocoder
from annoying.decorators import render_to
from datetime import datetime
from continents.models import CONTINENTS
from cities.models import City
import GeoIP

MINSK = [53.9, 27.566667]

class MongoJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return DjangoJSONEncoder.default(self, obj)
        

def get_location(request, default=MINSK):
    location = request.session.get('location', None)
    if location and len(str(location[0])) < 4:
        return location

    remote_addr = request.META['REMOTE_ADDR']
    if remote_addr == '127.0.0.1':
        request.session['location'] = default
        return default

    gi = GeoIP.open(settings.GEOIP_CITY, GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)
    geoip = gi.record_by_name(remote_addr)
    if not geoip:
        request.session['location'] = default
        return default

    time_zone = geoip.get('time_zone', None)
    if time_zone:
        request.session['django_timezone'] = pytz.timezone(time_zone)
    country = geoip.get('country_name', None)
    if country:
        request.session['country'] = country
    country_code = geoip.get('country_code', None)
    if country_code:
        request.session['country_code'] = country_code
    
    city = geoip.get('city', None)
    if city:
        request.session['city'] = city
        lat = geoip.get('latitude', None)
        lng = geoip.get('longitude', None)
        request.session['location'] = [lat, lng]
    else:
        request.session['city'] = 'Minsk'
        request.session['location'] = default
    # wtf ?
    return request.session['location']

def get_city(request, country_slug, city_slug):
    city = None
    if country_slug and city_slug:
        try:
            city = City.objects.get(slug=city_slug, country__slug=country_slug)
        except:
            pass
    if not city and 'city' in request.session and 'country_code' in request.session:
        try:
            city = City.objects.get(slug=slugify(request.session['city']), 
                                    country__code=request.session['country_code'])
        except:
            pass
    if not city and 'country_code' in request.session:
        city = City.objects.filter(country__code=request.session['country_code']).order_by('-population')[0]
    if not city:
        city = City.objects.get(slug='minsk', 
                                country__code='BY')
    return city
        

@render_to('index.html')
def homepage(request, country_slug=None, city_slug=None):
    location = get_location(request)
    city = get_city(request, country_slug, city_slug)
    center = [city.location[1], city.location[0]]
    checkins = list(get_checkins(center))
    checkins_json = json.dumps(checkins, cls=MongoJSONEncoder)
    continents = CONTINENTS
    return locals()


@render_to('user_feed.html')
def user_feed(request, username):
    the_user = get_object_or_404(User, username=username)
    db = get_checkins_db()
    user_feed = db.find(dict(username=username)).sort("timestamp", pymongo.DESCENDING)
    return locals()


@login_required
def locate(request):
    """ Ajax view. Locates user and creates a Checkin. """
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            try:
                the_checkin = form.save(request)
                request.session['location'] = the_checkin['location']
                data = json.dumps(the_checkin, cls=MongoJSONEncoder)
            except Exception, e:
                data = json.dumps({'error': str(e)})
        else:
            data = json.dumps({'error': form.errors})
    else:
        data = json.dumps({'error': 'Use POST.'})
    return HttpResponse(data)


def checkins(request, checkin_id=None):
    now = timezone.now().replace(hour=0, minute=1)
    db = get_checkins_db()

    if request.method == 'GET' and checkin_id:
        data = db.find_one({"_id": checkin_id})
        if not data:
            raise Http404

    elif request.method == 'GET' and not checkin_id:
        data = get_checkins(get_location(request))

    elif request.method == 'POST' and not checkin_id:
        post_data = json.loads(request.POST.keys()[0])
        form = LocationForm(data=post_data['location'])
        if form.is_valid():
            data = form.save(request, geocode=post_data['geocode'][0])
    
    return HttpResponse(json.dumps(data, cls=MongoJSONEncoder))

