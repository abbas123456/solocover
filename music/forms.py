from django.forms import ModelForm
from music.models import Track

class TrackForm(ModelForm):

    class Meta:
        model = Track
        exclude = ('album','track_number','length','name','artists')
