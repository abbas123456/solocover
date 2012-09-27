from songthread.services import SongthreadService
from django.test import TestCase
from music.models import Track


class SongthreadServiceTestCase(TestCase):
    
    def test_populate_track_using_spotify_lookup_returns_correct_results(self):
        track = Track
        track.spotify_uri = 'spotify:track:6NmXV4o6bmp704aPGyTVVG';
        songthread_service = SongthreadService()
        songthread_service.populate_track_using_spotify_lookup(track)
        self.assertEqual(u'B\xf8n Fra Helvete - Live', track.name)
        self.assertEqual(u'Mann Mot Mann (2002)', track.album)
        self.assertEqual(u'Kaizers Orchestra', track.artists)
        self.assertEqual(317.04000000000002, track.length)
        self.assertEqual(u'2', track.track_number)
        
    def test_make_spotify_api_call_returns_valid_json(self):
        track = Track
        track.spotify_uri = 'spotify:track:6NmXV4o6bmp704aPGyTVVG';
        songthread_service = SongthreadService()
        track_json = songthread_service.make_spotify_api_call(track)
        self.assertTrue('name' in track_json)
        self.assertTrue('album' in track_json)
        self.assertTrue('artists' in track_json)
        self.assertTrue('length' in track_json)
        self.assertTrue('track-number' in track_json)
        
        
        
    