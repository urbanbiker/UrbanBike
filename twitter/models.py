from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from tweepy import api
from tweepy.models import Model

SEARCH_RADIUS = '24km'

class TwitterJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Model):
            return obj.__dict__
        else:
            return DjangoJSONEncoder.default(self, obj)


def get_tweets(location):
    geocode = '%s,%s,%s' % (location[0], location[1], SEARCH_RADIUS)
    cache_key = 'twitter%s' % geocode
    search = cache.get(cache_key)
    if not search:
        try:
            # Ugly but we need to provide search query in different languages...
            # TODO: implement diffrent appproach after adding Twitter signup.
            query = Search.objects.all()[0].query
        except IndexError:
            query = 'bike OR bicycle'

        search = api.search(query, geocode=geocode)
        cache.set(cache_key, search)
    return search


class Search(models.Model):
    query = models.CharField(max_length=100)

    def __unicode__(self):
        return self.query
