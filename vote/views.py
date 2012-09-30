from vote.models import Vote
from datetime import datetime
from django.http import HttpResponseRedirect
from songthread.models import Song
from django.core.urlresolvers import reverse

def vote(request, song_id, like):
    vote = Vote()
    vote.song = Song.objects.get(id=song_id)
    if like == '1':
        vote.like = True
    else:
        vote.like = False
        
    vote.created_date = datetime.now()
    vote.user = request.user
    vote.save()
    return HttpResponseRedirect(get_success_url(vote))
    
def get_success_url(vote):
    return reverse('songthread_detail',
                       kwargs={'pk': vote.song.songthread.id})
