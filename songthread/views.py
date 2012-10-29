import urllib2
from datetime import datetime
from subprocess import CalledProcessError

from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, CreateView, ListView
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError

from songthread.forms import SongForm, CommentForm
from songthread.models import Song, Songthread, Comment
from songthread.services import SongthreadService
from music.forms import TrackForm
from vote.services import VoteService


SPOTIFY_EMBED_URL = 'https://embed.spotify.com/?uri='


class SongthreadListView(ListView):
    model = Songthread

    def get_context_data(self, **kwargs):
        context = super(SongthreadListView, self).get_context_data(**kwargs)
        context['spotify_embed_url'] = SPOTIFY_EMBED_URL
        context['latest_songthreads'] = Songthread.objects.all()\
            .order_by('-created_date')[0:5]
        context['top_users'] = User.objects.all()\
            .exclude(username='Anonymous')\
            .annotate(number_of_likes=Sum('song__vote__like'))\
            .order_by('number_of_likes')[0:4]
        return context


class SongthreadDetailView(DetailView):
    model = Songthread

    def get_context_data(self, **kwargs):
        context = super(SongthreadDetailView, self).get_context_data(**kwargs)
        context['spotify_embed_url'] = SPOTIFY_EMBED_URL
        songthread_id_kwarg = self.kwargs['pk']
        songs = Song.objects.filter(songthread_id=songthread_id_kwarg)\
                            .annotate(number_of_votes=Count('vote'),
                                      number_of_likes=Sum('vote__like'))\
                            .order_by('number_of_likes')
        vote_service = VoteService()
        for song in songs:
            song.vote = vote_service.get_users_vote_for_song(
                song, self.request.user)
        comments = Comment.objects.filter(songthread_id=songthread_id_kwarg)\
                                  .order_by('-created_date')
        context['songs'] = songs
        context['comments'] = comments
        context['anonymous_user'] = User.objects.get(username='Anonymous')
        return context


class SongthreadCreateView(CreateView):
    form_class = TrackForm
    template_name = 'songthread/songthread_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SongthreadCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SongthreadCreateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        track = form.save(commit=False)
        try:
            songthread_service = SongthreadService()
            songthread_service.populate_track_using_spotify_lookup(track)
        except urllib2.HTTPError:
            return HttpResponseRedirect(self.get_failure_url())
        track.save()
        songthread = Songthread()
        songthread.user = self.request.user
        songthread.created_date = datetime.now()
        songthread.track = track
        songthread.save()
        return HttpResponseRedirect(self.get_success_url(songthread))

    def get_success_url(self, songthread):
        return songthread.get_absolute_url()

    def get_failure_url(self):
        return reverse('songthread_list')


class SongCreateView(CreateView):
    form_class = SongForm
    model = Song

    def form_valid(self, form):
        try:
            song = form.save(commit=False)
            song.user = self.request.user
            song.created_date = datetime.now()
            songthread_id = self.kwargs['songthread_id']
            song.songthread = Songthread.objects.get(id=songthread_id)
            song.full_clean()
            song.save()
        except ValidationError as e:
            form._errors = ErrorList(e.message_dict['__all__'])
            return super(SongCreateView, self).form_invalid(form)
        except CalledProcessError:
            form._errors = ErrorList(('There was a problem converting '
                                      'your file to mp3 format',))
            return super(SongCreateView, self).form_invalid(form)

        return HttpResponseRedirect(self.get_success_url(song))

    def get_success_url(self, song):
        return song.songthread.get_absolute_url()


class CommentCreateView(CreateView):
    form_class = CommentForm
    model = Comment

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        songthread_id = self.kwargs['songthread_id']
        context['songthread_id'] = songthread_id
        return context

    def form_invalid(self, form):
        songthread_id = self.kwargs['songthread_id']
        songthread = Songthread.objects.get(id=songthread_id)
        if 'content' in form._errors:
            messages.add_message(self.request, messages.INFO,
                                 form._errors['content'])
        return HttpResponseRedirect(self.get_failure_url(songthread))

    def form_valid(self, form):
        if not self.request.user.is_authenticated():
            user = User.objects.get(username='Anonymous')
        else:
            user = self.request.user
        form.instance.user = user
        form.instance.created_date = datetime.now()
        songthread_id = self.kwargs['songthread_id']
        form.instance.songthread = Songthread.objects.get(id=songthread_id)
        comment = form.save()
        return HttpResponseRedirect(self.get_success_url(comment))

    def get_success_url(self, comment):
        return comment.songthread.get_absolute_url()

    def get_failure_url(self, songthread):
        return songthread.get_absolute_url()
