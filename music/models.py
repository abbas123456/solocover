from django.db import models

class Track(models.Model):
    album = models.CharField(max_length=128)
    track_number = models.IntegerField()
    length = models.FloatField()
    name = models.CharField(max_length=128)
    artists = models.CharField(max_length=256)
    spotify_uri = models.CharField(max_length=36,unique=True) # spotify:track:5RT0e9PkjBtmvqQzNbe1vA
    
    def __unicode__(self):
        return self.name