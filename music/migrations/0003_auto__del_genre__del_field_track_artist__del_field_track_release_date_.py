# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Genre'
        db.delete_table('music_genre')

        # Deleting field 'Track.artist'
        db.delete_column('music_track', 'artist')

        # Deleting field 'Track.release_date'
        db.delete_column('music_track', 'release_date')

        # Deleting field 'Track.genre'
        db.delete_column('music_track', 'genre_id')

        # Adding field 'Track.album'
        db.add_column('music_track', 'album',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=128),
                      keep_default=False)

        # Adding field 'Track.track_number'
        db.add_column('music_track', 'track_number',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Track.length'
        db.add_column('music_track', 'length',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Track.artists'
        db.add_column('music_track', 'artists',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=256),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Genre'
        db.create_table('music_genre', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('music', ['Genre'])

        # Adding field 'Track.artist'
        db.add_column('music_track', 'artist',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=128),
                      keep_default=False)

        # Adding field 'Track.release_date'
        db.add_column('music_track', 'release_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 8, 0, 0)),
                      keep_default=False)

        # Adding field 'Track.genre'
        db.add_column('music_track', 'genre',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='test', to=orm['music.Genre']),
                      keep_default=False)

        # Deleting field 'Track.album'
        db.delete_column('music_track', 'album')

        # Deleting field 'Track.track_number'
        db.delete_column('music_track', 'track_number')

        # Deleting field 'Track.length'
        db.delete_column('music_track', 'length')

        # Deleting field 'Track.artists'
        db.delete_column('music_track', 'artists')


    models = {
        'music.track': {
            'Meta': {'object_name': 'Track'},
            'album': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'artists': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'spotify_uri': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'track_number': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['music']