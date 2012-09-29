import wave
import contextlib
from mutagen.mp3 import MP3

from math import ceil
from django.forms import ModelForm
from django.conf import settings
from django.core.exceptions import ValidationError
from songthread.models import Song, Songthread
from mutagen.mp3 import MP3

class SongthreadForm(ModelForm):

    class Meta:
        model = Songthread
        exclude = ('user', 'created_date')
        
class SongForm(ModelForm):
    
    accepted_file_types = ['audio/mpeg', 'audio/x-wav']
    def clean_file(self):
        file_object = self.cleaned_data['file']
        file_path = file_object.temporary_file_path()
        if file_object.content_type not in self.accepted_file_types:
            raise ValidationError("You can only upload mp3 and wav files")
        
        if file_object.content_type =='audio/x-wav':
            with contextlib.closing(wave.open(file_path, 'r')) as f:
                number_of_frames = f.getnframes()
                frame_rate = f.getframerate()
                number_of_seconds = ceil(number_of_frames/float(frame_rate))
        if file_object.content_type =='audio/mpeg':            
            mp3_file = MP3(file_path)
            number_of_seconds = ceil(mp3_file.info.length)
             
        if number_of_seconds > 30 or number_of_seconds < 10:
            raise ValidationError("Your song needs to be between 10 and 30 seconds")
        else:
            return file_object
    class Meta:
        model = Song
        exclude = ('user', 'songthread','created_date')
        
