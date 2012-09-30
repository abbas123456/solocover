from vote.models import Vote
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class VoteForm(ModelForm):
    
    class Meta:
        model = Vote
        exclude = ('user', 'created_date', 'like', 'song')
        
    def clean(self):
        try:
            Vote.objects.get(song_id=self.instance.song.id)
            raise ValidationError("Vote already exists")
        except Vote.DoesNotExist:
            return self
        except Vote.MultipleObjectsReturned:
            raise Exception("Multiple votes exist")
