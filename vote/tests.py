"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from vote.services import VoteService
from django.test import TestCase
from vote.models import Vote
from django.contrib.auth.models import User
from songthread.models import Song
from datetime import datetime

class VoteServiceTest(TestCase):
    def test_has_user_voted_for_song(self):
        vote_service = VoteService()
        vote = Vote()
        vote.user_id = 1
        vote.song_id = 1
        vote.created_date = datetime.now()
        vote.like = True
        vote.save()
        user = User()
        user.id = 1
        song = Song
        song.id = 1
        self.assertTrue(vote_service.has_user_voted_for_song(song, user))
