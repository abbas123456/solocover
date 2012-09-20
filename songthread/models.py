from django.db import models
from django.contrib.auth.models import User

from music.models import Track

class Songthread(models.Model):
    name = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    track = models.ForeignKey(Track)
    
    def __unicode__(self):
        return self.name
    
class Song(models.Model):
    songthread = models.ForeignKey(Songthread)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.user
        


