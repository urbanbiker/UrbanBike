from googlegeocoder import GoogleGeocoder, BaseAPIObject, AddressComponent
from django.utils.encoding import force_unicode

class GeocoderResult(BaseAPIObject):
    def __init__(self, d):
        self.__dict__ = d
        self.address_components = [AddressComponent(i) for i in self.address_components]
        
    def __unicode__(self):
        return unicode(self.formatted_address)


def get_address(d):
    address = {}
    return set_fields(GeocoderResult(d), address)

def set_fields(search, address):
    address['formatted_address'] = force_unicode(search.formatted_address)
    for component in search.address_components:
        if 'route' in component.types:
            if address.get('street', None):
                address['street'] += ' ' + force_unicode(component.long_name)
            else:
                address['street'] = force_unicode(component.long_name)
        if 'locality' in component.types:
            address['city'] = force_unicode(component.long_name)
        if 'country' in component.types:
            address['country'] = force_unicode(component.long_name)
        if 'postal_code' in component.types:
            address['postal_code'] = component.long_name
        if 'administrative_area_level_1' in component.types:
            address['state'] = component.short_name
        if 'street_number' in component.types:
            address['street'] = component.short_name
    return address


def reverse_geocode(lat, lng):
    geocoder = GoogleGeocoder()
    address = {}
    try:
        search = geocoder.get((lat, lng))[0]
        address = set_fields(search, address)
        address['geocode_status'] = 'success'
    except ValueError, IndexError:
        address['geocode_status'] = 'failed'
    return address
