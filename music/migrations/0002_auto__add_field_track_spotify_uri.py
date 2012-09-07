# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Track.spotify_uri'
        db.add_column('music_track', 'spotify_uri',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=32),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Track.spotify_uri'
        db.delete_column('music_track', 'spotify_uri')


    models = {
        'music.genre': {
            'Meta': {'object_name': 'Genre'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'music.track': {
            'Meta': {'object_name': 'Track'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['music.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'spotify_uri': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['music']