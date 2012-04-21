from django.contrib.gis.feeds import GeoRSSFeed
from django.contrib.syndication.views import Feed
from django.contrib.humanize.templatetags import humanize
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils import feedgenerator
from django.template.defaultfilters import slugify
from django.utils.xmlutils import SimplerXMLGenerator

from checkins.models import todays_stuff
from checkins.views import get_location

class KmlFeed(feedgenerator.SyndicationFeed):
    ns = u"http://www.opengis.net/kml/2.2"
    mime_type = u"application/vnd.google-earth.kml+xml"
    
    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement(u'kml', self.root_attributes())
        handler.startElement(u'Document', {})
        self.add_root_elements(handler)
        self.write_styles(handler)
        self.write_items(handler)
        handler.endElement(u"Document")
        handler.endElement(u"kml")

    def root_attributes(self):
        return {u"xmlns": self.ns}

    def add_root_elements(self, handler):
        handler.addQuickElement(u"name", self.feed['title'])
        handler.addQuickElement(u"description", self.feed['description'])

    def write_items(self, handler):
        for item in self.items:
            handler.startElement(u'Placemark', {})
            self.add_item_elements(handler, item)
            handler.endElement(u"Placemark")

    def write_styles(self, handler):
        for item in self.items:
            self.add_item_style(handler, item)

    def add_item_elements(self, handler, item):
        handler.addQuickElement(u"name", item['title'])
        handler.addQuickElement(u"description", item['description'])
        self.add_location(handler, item)
        self.add_style(handler, item)

    def add_item_style(self, handler, item):
        handler.startElement(u'Style', {'id': item['id']})
        handler.startElement(u'IconStyle', {})
        handler.startElement(u'Icon', {})
        handler.addQuickElement(u'href', item['avatar'])
        handler.endElement(u"Icon")
        handler.endElement(u"IconStyle")
        handler.endElement(u"Style")

    def add_location(self, handler, item):
        geom = item.get('geometry', None)
        if geom and isinstance(geom, (list, tuple)):
            if len(geom) == 2:
                handler.startElement(u'Point', {})
                handler.addQuickElement(u'coordinates', '%s,%s'  % (geom[1], geom[0]))
                handler.endElement(u"Point")

    def add_style(self, handler, item):
        handler.addQuickElement(u'styleUrl', '#' + item['id'])


class CheckinsFeed(Feed):
    feed_type = KmlFeed
    title = "Bicycling Checkins"
    link = '/kml/'
    description = "Today's People Checkins."
    description_template = 'checkin_kml.html'


    def get_object(self, request, city=None):
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        if lat and lng:
            return [lat, lng]
        return get_location(request)

    def items(self, obj):
        return todays_stuff(obj)

    def item_link(self, obj):
        return '/kml/'

    def feed_url(self):
        return '/kml/'

    def item_title(self, item):
        if hasattr(item, 'full_name'):
            return item['full_name']
        if hasattr(item, 'user'):
            return item.user.username
        if hasattr(item, 'from_user_name'):
            return item.from_user_name
    
                    
    def item_icon(self, item):
        if hasattr(item, 'avatar'):
            return item['avatar']
        if hasattr(item, 'user'):
            return item.user.profile_picture
        if hasattr(item, 'profile_image_url'):
            return item.profile_image_url


    def item_geometry(self, item):
        if hasattr(item, 'location'):
            location = getattr(item, 'location')
            if isinstance(location, (list, tuple)):
                return location
            if hasattr(location, 'point'):
                return [location.point.latitude, location.point.longitude]
        if hasattr(item, 'geo'):
            geo = item.geo
            return geo['coordinates']


    def item_guid(self, item):
        if hasattr(item, 'id'):
            return str(getattr(item, 'id'))
        return str(item['_id'])

    def item_extra_kwargs(self, item):
        return {'geometry' : self.item_geometry(item),
                'avatar': self.item_icon(item),
                'id': str(self.item_guid(item))}

