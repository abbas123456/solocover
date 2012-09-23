from django.forms import ModelForm
from songthread.models import Song, Songthread

class SongthreadForm(ModelForm):

    class Meta:
        model = Songthread
        exclude = ('user', 'created_date')
        
class SongForm(ModelForm):

    class Meta:
        model = Song
        exclude = ('user', 'songthread','created_date')
        
