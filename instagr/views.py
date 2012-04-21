from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.http import HttpResponse

from instagr.models import InstagrJSONEncoder, get_media

def photos(request):
    location = (request.GET['lat'], request.GET['lng'])
    search = get_media(location)
    return HttpResponse(json.dumps(search, cls=InstagrJSONEncoder))

