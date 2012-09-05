# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Genre'
        db.create_table('music_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('music', ['Genre'])

        # Adding model 'Track'
        db.create_table('music_track', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('genre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Genre'])),
        ))
        db.send_create_signal('music', ['Track'])


    def backwards(self, orm):
        # Deleting model 'Genre'
        db.delete_table('music_genre')

        # Deleting model 'Track'
        db.delete_table('music_track')


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
            'release_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['music']