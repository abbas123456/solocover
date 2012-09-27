from django.forms import ModelForm
from music.models import Track
from django.core.exceptions import ValidationError
from songthread.services import SPOTIFY_LOOKUP_URL

import urllib2

class TrackForm(ModelForm):
    
    def clean_spotify_uri(self):
        spotify_uri = self.cleaned_data['spotify_uri']
        try:
            urllib2.urlopen('{0}{1}'.format(SPOTIFY_LOOKUP_URL, spotify_uri))
        except urllib2.HTTPError:
            raise ValidationError("The spotify uri does not exist")
        
        return spotify_uri

    class Meta:
        model = Track
        exclude = ('album','track_number','length','name','artists')


