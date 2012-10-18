from mutagen.mp3 import MP3

from math import ceil
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from songthread.models import Song, Songthread, Comment

class SongthreadForm(ModelForm):

    class Meta:
        model = Songthread
        exclude = ('user', 'created_date')

class SongForm(ModelForm):
    
    accepted_file_types = ['audio/mpeg']
    def clean_file(self):
        file_object = self.cleaned_data['file']
        file_path = file_object.temporary_file_path()
        if file_object.content_type not in self.accepted_file_types:
            raise ValidationError("Your song needs to be in mp3 format")
        
        if file_object.content_type =='audio/mpeg':            
            mp3_file = MP3(file_path)
            number_of_seconds = ceil(mp3_file.info.length)
             
        if number_of_seconds > 180:
            raise ValidationError("Your song needs to be three minutes or less")
        else:
            return file_object
    class Meta:
        model = Song
        exclude = ('user', 'songthread','created_date', 'file_content_type')
        

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'created_date', 'songthread')
        
    def clean_content(self):
        return self.cleaned_data['content']