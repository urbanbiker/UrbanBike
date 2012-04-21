# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Search'
        db.create_table('twitter_search', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('twitter', ['Search'])


    def backwards(self, orm):
        
        # Deleting model 'Search'
        db.delete_table('twitter_search')


    models = {
        'twitter.search': {
            'Meta': {'object_name': 'Search'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['twitter']
