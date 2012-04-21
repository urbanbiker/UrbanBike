from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.http import HttpResponse

from twitter.models import get_tweets, TwitterJSONEncoder

def tweets(request):
    location = (request.GET['lat'], request.GET['lng'])
    search = get_tweets(location)
    return HttpResponse(json.dumps(search, cls=TwitterJSONEncoder))

