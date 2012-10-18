from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from solocover.settings import STATIC_URL
from PIL import Image #@UnresolvedImport

THUMBNAIL_SIZE = 350, 350

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_image = models.FileField(upload_to = 'images/')
    about_me = models.CharField(max_length=512)
    location = models.CharField(max_length=64)
    likes = models.CharField(max_length=128)
    dislikes = models.CharField(max_length=128)
    
    def get_profile_image_path(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return "{0}{1}".format(STATIC_URL, 'img/anon.jpeg')
    
    def save(self, *args, **kwargs):
        super(UserProfile, self).save()
        if self.profile_image:
            image = Image.open(self.profile_image.path)
            image.thumbnail(THUMBNAIL_SIZE,Image.ANTIALIAS)
            image.save(self.profile_image.path)
            
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile()
        user_profile.user = instance
        user_profile.save()

post_save.connect(create_user_profile, sender=User)

