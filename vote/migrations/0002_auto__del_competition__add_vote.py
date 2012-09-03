# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Competition'
        db.delete_table('vote_competition')

        # Adding model 'Vote'
        db.create_table('vote_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('vote', ['Vote'])


    def backwards(self, orm):
        # Adding model 'Competition'
        db.create_table('vote_competition', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('vote', ['Competition'])

        # Deleting model 'Vote'
        db.delete_table('vote_vote')


    models = {
        'vote.vote': {
            'Meta': {'object_name': 'Vote'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['vote']