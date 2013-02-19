# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'URLChangeRecord.old_url'
        db.alter_column('url_tracker_urlchangerecord', 'old_url', self.gf('django.db.models.fields.TextField')(unique=True))

        # Changing field 'URLChangeRecord.new_url'
        db.alter_column('url_tracker_urlchangerecord', 'new_url', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'URLChangeRecord.old_url'
        db.alter_column('url_tracker_urlchangerecord', 'old_url', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True))

        # Changing field 'URLChangeRecord.new_url'
        db.alter_column('url_tracker_urlchangerecord', 'new_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    models = {
        'url_tracker.urlchangerecord': {
            'Meta': {'object_name': 'URLChangeRecord'},
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'old_url': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['url_tracker']