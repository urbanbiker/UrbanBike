from django.db import models
from django.conf import settings
from django.utils import timezone

import pymongo
from facebook.models import FacebookProfile
from sorl.thumbnail import get_thumbnail
from instagr.models import get_media
from twitter.models import get_tweets  
from itertools import chain

import logging
logger = logging.getLogger(__name__)


class UserProfile(FacebookProfile):
    """ User Profile Wrapper. TODO: migrate to social_auth."""

    class Meta:
        proxy = True

    def get_avatar(self):
        return get_thumbnail('http://graph.facebook.com/%s/picture' % self.facebook_id, '50')

def get_checkins_db():
    return pymongo.Connection(settings.MONGODB_HOST,
                              settings.MONGODB_PORT).ramacarbon['checkins']

def get_checkins(center, radius=10, start_time=timezone.now().replace(hour=0, minute=1)):
    try:
        db = get_checkins_db()
    except:
        logger.error('MongoDB is down!')
        return []

    if center[1] > 90 or center[1] < -90:
        # stupid fix: exchange coordinates.
        center = [center[1], center[0]]
    return db.find(dict(location={"$nearSphere": center, 
                                  '$maxDistance': radius/111.12},
                        timestamp={'$gte': start_time})).sort("timestamp", pymongo.ASCENDING)

def todays_checkins(start_time=timezone.now().replace(hour=0, minute=1)):
    db = get_checkins_db()
    return db.find(dict(timestamp={'$gte': start_time}))

def todays_stuff(location):
    all_today_checkins = todays_checkins()
    instagram_photos = get_media(location)
    twitts = filter(lambda x: x.geo, get_tweets(location))
    return chain(all_today_checkins, instagram_photos, twitts)


#pymongo.Connection().ramacarbon['checkins'].ensure_index([("location", pymongo.GEO2D)])
#pymongo.Connection().ramacarbon['checkins'].ensure_index([("timestamp", pymongo.DESCENDING), 
#                                                          ("username", pymongo.ASCENDING)])
