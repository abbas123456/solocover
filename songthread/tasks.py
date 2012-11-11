from twitter import *
from solocover.settings import TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from celery import task #@UnresolvedImport
from django.contrib.sites.models import Site

@task()
def tweet_about_new_songthread(songthread):
    current_site = Site.objects.get_current()
    twitter = Twitter(auth=OAuth(TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)) #@UndefinedVariable
    twitter.statuses.update(status="A new thread has just been started by {0}, check it out on {1}{2}".format(songthread.user, current_site.domain, songthread.get_absolute_url()))

@task()
def tweet_about_new_song(song):
    current_site = Site.objects.get_current()
    twitter = Twitter(auth=OAuth(TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)) #@UndefinedVariable
    twitter.statuses.update(status="A new song entry has just been submitted by {0}, check it out on {1}{2}".format(song.songthread.user, current_site.domain, song.songthread.get_absolute_url()))

@task()
def tweet_about_new_comment(comment):
    current_site = Site.objects.get_current()
    twitter = Twitter(auth=OAuth(TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)) #@UndefinedVariable
    twitter.statuses.update(status="A new comment has been added by {0}, check it out on {1}{2}".format(comment.user, current_site.domain, comment.songthread.get_absolute_url()))


