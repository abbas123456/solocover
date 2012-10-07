from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_image = models.FileField(upload_to = 'images/')
    about_me = models.CharField(max_length=256) 

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile()
        user_profile.user = instance
        user_profile.save()

post_save.connect(create_user_profile, sender=User)

