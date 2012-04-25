from django.db import models, IntegrityError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel
import uuid
import pymongo

class MongoDBTraceManager(object):
    
    @property
    def db(self):
        return pymongo.Connection(
            settings.MONGODB_HOST,
            settings.MONGODB_PORT).urbanbike['traces']

    def find_one(self, spec):
        return db.find_one(spec)

    def create(uuid):
        the_trace = dict(uuid=uuid, points=[])
        db.insert(the_trace)
        return the_trace
        

class Trace(TimeStampedModel):
    user = models.ForeignKey(User, related_name='traces', null=True, blank=True)
    # URL-friendly thread UD.
    uuid = models.CharField(max_length=8, editable=False, unique=True, db_index=True)

    title = models.CharField(_('title'), max_length=255, blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)

    where_start = models.CharField(_('start'), max_length=255, blank=True, null=True)
    where_end = models.CharField(_('end'), max_length=255, blank=True, null=True)

    mongo_objects = MongoDBTraceManager()

    def __unicode__(self):
        return self.title or self.uuid

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())[:4]
        try:
            super(Trace, self).save(*args, **kwargs)
        except IntegrityError:
            self.uuid = None
            self.save(*args, **kwargs)

