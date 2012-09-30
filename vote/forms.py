from vote.models import Vote
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from vote.services import VoteService

class VoteForm(ModelForm):
    
    class Meta:
        model = Vote
        exclude = ('song', 'user', 'created_date')
        
    def clean(self):
        vote_service = VoteService()
        if vote_service.has_user_voted_for_song(self.instance.song, self.instance.user):
            raise ValidationError("Vote already exists")
        else:
            return self
