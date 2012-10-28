from vote.models import Vote
from datetime import datetime
from django.http import HttpResponseRedirect
from songthread.models import Song
from django.core.urlresolvers import reverse
from vote.forms import VoteForm
from django.views.generic import CreateView
from vote.services import VoteService


class VoteCreateView(CreateView):
    form_class = VoteForm
    model = Vote

    def get_initial(self):
        initial = super(VoteCreateView, self).get_initial()
        initial['song'] = Song.objects.get(id=self.kwargs['song_id'])
        initial['like'] = True if self.kwargs['like'] == '1' else False
        initial['user'] = self.request.user
        return initial

    def get(self, request, *args, **kwargs):
        form = VoteForm(data=request.GET, initial=self.get_initial())
        if form.is_valid():
            vote = self.process_form(form)
            return HttpResponseRedirect(self.get_success_url(vote))
        else:
            return HttpResponseRedirect(self.get_failure_url())

    def form_valid(self, form):
        vote = self.process_form(form)
        return HttpResponseRedirect(self.get_success_url(vote))

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_failure_url())

    def process_form(self, form):
        form.instance.song = form.song
        form.instance.like = form.like
        form.instance.user = form.user
        form.instance.created_date = datetime.now()
        vote = form.save()
        return vote

    def get_success_url(self, vote):
        return vote.song.songthread.get_absolute_url()

    def get_failure_url(self):
        return reverse('songthread_list')
