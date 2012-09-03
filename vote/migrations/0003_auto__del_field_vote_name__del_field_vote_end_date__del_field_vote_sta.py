# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Vote.name'
        db.delete_column('vote_vote', 'name')

        # Deleting field 'Vote.end_date'
        db.delete_column('vote_vote', 'end_date')

        # Deleting field 'Vote.start_date'
        db.delete_column('vote_vote', 'start_date')

        # Adding field 'Vote.score'
        db.add_column('vote_vote', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Vote.comment'
        db.add_column('vote_vote', 'comment',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=64),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Vote.name'
        db.add_column('vote_vote', 'name',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=128),
                      keep_default=False)

        # Adding field 'Vote.end_date'
        db.add_column('vote_vote', 'end_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Vote.start_date'
        db.add_column('vote_vote', 'start_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 3, 0, 0)),
                      keep_default=False)

        # Deleting field 'Vote.score'
        db.delete_column('vote_vote', 'score')

        # Deleting field 'Vote.comment'
        db.delete_column('vote_vote', 'comment')


    models = {
        'vote.vote': {
            'Meta': {'object_name': 'Vote'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['vote']