from django.forms import ModelForm
from django.core.exceptions import ValidationError
from songthread.models import Song, Songthread, Comment

mp3_file_types = ['audio/mpeg', 'audio/mp3']


class SongthreadForm(ModelForm):

    class Meta:
        model = Songthread
        exclude = ('user', 'created_date')


class SongForm(ModelForm):
    class Meta:
        model = Song
        exclude = ('user', 'songthread', 'created_date')

    def clean_file(self):
        file_object = self.cleaned_data['file']
        file_type = file_object.content_type.split('/')[0]
        if file_type != 'audio':
            raise ValidationError("Your song needs to be in audio format")

        return file_object


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'created_date', 'songthread')
