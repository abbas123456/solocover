# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Track.spotify_uri'
        db.alter_column('music_track', 'spotify_uri', self.gf('django.db.models.fields.CharField')(max_length=36))

        # Changing field 'Track.length'
        db.alter_column('music_track', 'length', self.gf('django.db.models.fields.FloatField')())

    def backwards(self, orm):

        # Changing field 'Track.spotify_uri'
        db.alter_column('music_track', 'spotify_uri', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'Track.length'
        db.alter_column('music_track', 'length', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'music.track': {
            'Meta': {'object_name': 'Track'},
            'album': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'artists': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'spotify_uri': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'track_number': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['music']