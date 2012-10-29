from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.files import File
from subprocess import CalledProcessError

from music.models import Track

import mimetypes
import subprocess
import os


class Songthread(models.Model):
    track = models.OneToOneField(Track)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField()
    slug = models.SlugField()

    def __unicode__(self):
        return self.track.name

    def save(self, *args, **kwargs):
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
    file = models.FileField(upload_to='songs/')
    created_date = models.DateTimeField()

    class Meta:
        unique_together = ('songthread', 'user',)

    def __unicode__(self):
        return self.songthread.track.name

    def save(self, *args, **kwargs):
        super(Song, self).save(*args, **kwargs)
        from songthread.forms import mp3_file_types
        if mimetypes.guess_type(self.file.path)[0] not in mp3_file_types:
            current_file_path = self.file.path
            new_file_path = current_file_path + '.mp3'
            try:
                subprocess.check_call(
                    ["ffmpeg", "-y", "-i", current_file_path, new_file_path],
                    stderr=subprocess.PIPE)
                new_file = File(open(new_file_path))
                self.file.save(self.file.name + '.mp3', new_file)
                os.remove(new_file.name)
            except CalledProcessError:
                self.delete()
                raise


class Comment(models.Model):
    songthread = models.ForeignKey(Songthread)
    user = models.ForeignKey(User)
    content = models.TextField()
    in_reply_to = models.ForeignKey('self', blank=True, null=True)
    created_date = models.DateTimeField()
