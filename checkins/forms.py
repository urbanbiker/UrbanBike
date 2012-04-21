from django import forms
from django.contrib.humanize.templatetags import humanize
from django.utils import timezone

from checkins.models import get_checkins_db
from checkins import geocoder

from datetime import datetime

class LocationForm(forms.Form):
    lat = forms.FloatField()
    lng = forms.FloatField()

    def save(self, request, geocode=None):
        data = self.cleaned_data
        the_checkin = dict(username=request.user.username,
                           timestamp=timezone.now(),
                           remote_addr=request.META['REMOTE_ADDR'])
        the_checkin['location'] = [data['lat'], data['lng']]
        the_checkin['avatar'] = request.user.get_profile().get_avatar().url
        the_checkin['full_name'] = request.user.get_full_name()
        the_checkin['naturaltime'] = humanize.naturaltime(the_checkin['timestamp'])
        if geocode:
            the_checkin.update(geocoder.get_address(geocode))
        else:
            the_checkin.update(geocoder.reverse_geocode(data['lat'], data['lng']))
        db = get_checkins_db()
        db.insert(the_checkin)
        the_checkin['id'] = the_checkin['_id']
        return the_checkin
        

