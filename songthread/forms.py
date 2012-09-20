from django.forms import ModelForm
from django.db.models import get_model

Song = get_model('songthread', 'song')


class SongForm(ModelForm):

    class Meta:
        model = Song
        exclude = ('user', 'songthread','created_date')