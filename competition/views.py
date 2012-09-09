from django.views.generic import DetailView,CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class CompetitionDetailView(DetailView):
    
    def get_context_data(self, **kwargs):
        context = super(CompetitionDetailView, self).get_context_data(**kwargs)
        context['spotify_embed_url'] = 'https://embed.spotify.com/?uri='
        return context


class SongCreateView(CreateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SongCreateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(SongCreateView, self).form_valid(form)