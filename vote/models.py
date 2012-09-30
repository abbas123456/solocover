from django.db import models
from songthread.models import Song

class Vote(models.Model):
    like = models.BooleanField()
    song = models.ForeignKey(Song)
    created_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.song.songthread.track.name