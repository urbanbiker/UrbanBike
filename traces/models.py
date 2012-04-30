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
        

class Trace(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    user = models.ForeignKey(User, related_name='traces', null=True, blank=True)
    # URL-friendly thread UD.
    uuid = models.CharField(max_length=8, editable=False, unique=True, db_index=True)

    title = models.CharField(_('title'), max_length=255, blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)

    where_start = models.CharField(_('start'), max_length=255, blank=True, null=True)
    where_end = models.CharField(_('end'), max_length=255, blank=True, null=True)

    mongo_objects = MongoDBTraceManager()

    def center(self):
        try:
            first_point = Trace.mongo_objects.db.find_one(
                dict(uuid=self.uuid))['points'][0]
            return '%s,%s' % (first_point['lat'], first_point['lng'])
        except IndexError:
            pass

    def points(self):
        obj = Trace.mongo_objects.db.find_one(dict(uuid=self.uuid))
        return 'color:0x0000ff|weight:5|' + '|'.join([','.join((str(p['lat']), str(p['lng']))) for p in obj['points']])


    def __unicode__(self):
        return self.title or self.uuid

    def get_start(self):
        obj = Trace.mongo_objects.db.find_one(dict(uuid=self.uuid))
        addresses = filter(lambda x: x.get('formatted_address', None), obj['points'])
        if addresses:
            return addresses[0]['formatted_address']


    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())[:4]
        try:
            super(Trace, self).save(*args, **kwargs)
        except IntegrityError:
            self.uuid = None
            self.save(*args, **kwargs)

    class Meta:
        get_latest_by = 'modified'
        ordering = ('-modified', '-created',)


