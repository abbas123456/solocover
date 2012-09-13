from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView,CreateView
from datetime import datetime

from competition.forms import SongForm
from competition.models import Song

class CompetitionDetailView(DetailView):
    
    def get_context_data(self, **kwargs):
        context = super(CompetitionDetailView, self).get_context_data(**kwargs)
        context['spotify_embed_url'] = 'https://embed.spotify.com/?uri='
        return context


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
        song = form.save()
        return HttpResponseRedirect(self.get_success_url(song))
    
    def get_success_url(self, song):
        return reverse('competition_detail',
                           kwargs={'pk': song.competition.id})