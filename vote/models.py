from django.db import models
from songthread.models import Song
from django.contrib.auth.models import User

class Vote(models.Model):
    like = models.BooleanField()
    song = models.ForeignKey(Song)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.song.songthread.track.name