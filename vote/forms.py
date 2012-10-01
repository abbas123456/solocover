from vote.models import Vote
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from vote.services import VoteService
from songthread.models import Song
from django.contrib.admin.models import User

class VoteForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs['initial']['user']
        self.song = kwargs['initial']['song']
        super(VoteForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Vote
        exclude = ('song', 'user', 'created_date')
        
    def clean(self):
        vote_service = VoteService()
        if vote_service.has_user_voted_for_song(self.song, self.user):
            raise ValidationError("Vote already exists")
        else:
            return self