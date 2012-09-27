import urllib2

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView,CreateView
from datetime import datetime

from songthread.forms import SongForm
from songthread.models import Song, Songthread
from songthread.services import SongthreadService

from music.forms import TrackForm

class SongthreadDetailView(DetailView):
    model=Songthread
    
    def get_context_data(self, **kwargs):
        context = super(SongthreadDetailView, self).get_context_data(**kwargs)
        context['spotify_embed_url'] = 'https://embed.spotify.com/?uri='
        songthread_id_kwarg =self.kwargs['pk']
        context['songs'] = Song.objects.filter(songthread_id=songthread_id_kwarg)
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
            return HttpResponseRedirect(self.get_success_url())    
        track.save()
        songthread = Songthread()
        songthread.user = self.request.user
        songthread.created_date = datetime.now()
        songthread.track = track
        songthread.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('songthread_list')
    
class SongCreateView(CreateView):
    form_class = SongForm
    model = Song    
    context_object_name = 'song'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SongCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created_date = datetime.now()
        songthread_id =self.kwargs['songthread_id']
        form.instance.songthread = Songthread.objects.get(id=songthread_id) 
        song = form.save()
        return HttpResponseRedirect(self.get_success_url(song))
    
    def get_success_url(self, song):
        return reverse('songthread_detail',
                           kwargs={'pk': song.songthread.id})
