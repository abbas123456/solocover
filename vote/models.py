from django.db import models
from songthread.models import Song
from django.contrib.auth.models import User


class Vote(models.Model):
    song = models.ForeignKey(Song)
    user = models.ForeignKey(User)
    like = models.BooleanField()
    created_date = models.DateTimeField()

    def __unicode__(self):
        return self.song.songthread.track.name
