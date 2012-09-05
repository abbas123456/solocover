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
    
    def __unicode__(self):
        return self.name