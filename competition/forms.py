from django.forms import ModelForm
from django.db.models import get_model

Song = get_model('competition', 'song')


class SongForm(ModelForm):

    class Meta:
        model = Song
        exclude = ('user', 'competition','created_date')