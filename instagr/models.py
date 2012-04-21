from django.conf import settings
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder

from instagram import client, InstagramAPIError
from instagram.models import ApiModel

class InstagrJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ApiModel):
            return obj.__dict__
        else:
            return DjangoJSONEncoder.default(self, obj)


def get_media(location, redirect_uri=None):
    api = client.InstagramAPI(client_id=settings.INSTAGRAM_CLIENT_ID,
                              client_secret=settings.INSTAGRAM_PRIVATE,
                              redirect_uri=redirect_uri)
    cache_key = 'instagram%s,%s' % (location[0], location[1])
    search = cache.get(cache_key)
    if not search:
        search = api.media_search(lat=location[0], 
                                  lng=location[1],
                                  distance=5000,
                                  count=settings.INSTAGRAM_MAX_OBJ_COUNT)
        cache.set(cache_key, search)
    return search

