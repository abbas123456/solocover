from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from music.models import Track

class Songthread(models.Model):
    track = models.OneToOneField(Track)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField()
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.track.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.track.name)
        return super(Songthread, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('songthread_detail', (), {
            'slug': self.slug,
            'pk': self.id,
        })

class Song(models.Model):
    songthread = models.ForeignKey(Songthread)
    user = models.ForeignKey(User)
    file = models.FileField(upload_to = 'songs/')
    created_date = models.DateTimeField()
    
    class Meta:
        unique_together = ('songthread', 'user',)
    
    def __unicode__(self):
        return self.songthread.track.name

class Comment(models.Model):
    songthread = models.ForeignKey(Songthread)
    user = models.ForeignKey(User)
    content = models.TextField()
    in_reply_to = models.ForeignKey('self', blank=True, null=True)
    created_date = models.DateTimeField()
        
    
        


