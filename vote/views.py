from vote.models import Vote
from datetime import datetime
from django.http import HttpResponseRedirect
from songthread.models import Song
from django.core.urlresolvers import reverse
from vote.forms import VoteForm

def vote(request, song_id):
    form = VoteForm(data=request.POST)
    song = Song.objects.get(id=song_id)
    form.instance.song = song 
    form.instance.user = request.user
    form.instance.created_date = datetime.now()
    if form.is_valid():
        vote = form.save()
    return HttpResponseRedirect(get_success_url(song))
    
def get_success_url(song):
    return reverse('songthread_detail',
                       kwargs={'pk': song.songthread.id})
