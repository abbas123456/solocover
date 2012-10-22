from django.forms import ModelForm
from django.core.exceptions import ValidationError
from songthread.models import Song, Songthread, Comment

class SongthreadForm(ModelForm):

    class Meta:
        model = Songthread
        exclude = ('user', 'created_date')

class SongForm(ModelForm):
    
    accepted_file_types = ['audio/mpeg', 'audio/mp3']
    
    class Meta:
        model = Song
        exclude = ('user','songthread','created_date')
        
    def clean_file(self):
        file_object = self.cleaned_data['file']
        if file_object.content_type not in self.accepted_file_types:
            raise ValidationError("Your song needs to be in mp3 format")
        else:
            return file_object
    
        

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'created_date', 'songthread')