from django.db import models
from django.contrib.auth.models import User

from music.models import Track

class Songthread(models.Model):
    track = models.OneToOneField(Track)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.track.name
    
class Song(models.Model):
    songthread = models.ForeignKey(Songthread)
    user = models.OneToOneField(User)
    file = models.FileField(upload_to = 'songs/')
    created_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.songthread.track.name

class Comment(models.Model):
    songthread = models.ForeignKey(Songthread)
    user = models.ForeignKey(User)
    content = models.TextField()
    in_reply_to = models.ForeignKey('self', blank=True, null=True)
    created_date = models.DateTimeField()
        
    
        


