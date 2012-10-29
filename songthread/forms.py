from django.forms import ModelForm
from django.core.exceptions import ValidationError
from songthread.models import Song, Songthread, Comment
import re
import subprocess

class SongthreadForm(ModelForm):

    class Meta:
        model = Songthread
        exclude = ('user', 'created_date')

class SongForm(ModelForm):
    
    mp3_file_types = ['audio/mpeg', 'audio/mp3']
    
    class Meta:
        model = Song
        exclude = ('user', 'songthread', 'created_date')
        
    def clean_file(self):
        file_object = self.cleaned_data['file']
        file_type = re.search('.*/', file_object.content_type).group()[:-1]
        if file_object.content_type not in self.mp3_file_types and file_type != 'audio':
            raise ValidationError("Your song needs to be in audio format")
        if file_object.content_type not in self.mp3_file_types:
            current_file_path = file_object.temporary_file_path() 
            new_file_path = current_file_path + '.mp3'
            response = subprocess.call(["ffmpeg", "-y", "-i", current_file_path, new_file_path], stderr=subprocess.PIPE)
            if response == 1:
                raise ValidationError("Could not convert to mp3 format, please do this and re-upload")

        return file_object
        
        

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'created_date', 'songthread')
