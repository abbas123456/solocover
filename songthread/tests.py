from views import SongthreadCreateView
from django.test import TestCase
from music.models import Track


class ViewsTestCase(TestCase):
    
    def test_populate_track_using_spotify_lookup_returns_correct_results(self):
        track = Track
        track.spotify_uri = 'spotify:track:6NmXV4o6bmp704aPGyTVVG';
        view = SongthreadCreateView() 
        view.populate_track_using_spotify_lookup(track)
        self.assertEqual(u'B\xf8n Fra Helvete - Live', track.name)
        self.assertEqual(u'Mann Mot Mann (2002)', track.album)
        self.assertEqual(u'Kaizers Orchestra', track.artists)
        self.assertEqual(317.04000000000002, track.length)
        self.assertEqual(u'2', track.track_number)
        
    