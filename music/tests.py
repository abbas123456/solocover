from django.test import TestCase
from forms import TrackForm
from models import Track

class FormsTestCase(TestCase):
    
    def test_form_with_valid_spotify_uri_is_valid(self):
        post_dict = {'spotify_uri': 'spotify:track:5RT0e9PkjBtmvqQzNbe1vA'}
        form = TrackForm(post_dict)
        self.assertTrue(form.is_valid())
        
    def test_form_with_invalid_spotify_uri_is_invalid(self):
        post_dict = {'spotify_uri': 'spotify:track:5RTe9PkjBtmvqQzNbe1vA'}
        form = TrackForm(post_dict)
        self.assertFalse(form.is_valid())
        
    def test_form_with_random_text_is_invalid(self):
        post_dict = {'spotify_uri': 'hello'}
        form = TrackForm(post_dict)
        self.assertFalse(form.is_valid())
