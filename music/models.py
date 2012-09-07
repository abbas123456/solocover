from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256) 
    
    def __unicode__(self):
        return self.name
 
class Track(models.Model):
    name = models.CharField(max_length=128)
    artist = models.CharField(max_length=128)
    release_date = models.DateTimeField()
    genre = models.ForeignKey(Genre)
    spotify_uri = models.CharField(max_length=32) # example of a web service call to get track information
                                                  # = http://ws.spotify.com/lookup/1/.json?uri=spotify:track:5RT0e9PkjBtmvqQzNbe1vA
    
    def __unicode__(self):
        return self.name