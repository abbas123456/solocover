import urllib2
import json

SPOTIFY_LOOKUP_URL = "http://ws.spotify.com/lookup/1/.json?uri="

class SongthreadService():
    
    def populate_track_using_spotify_lookup(self, track):
        track_json = self.make_spotify_api_call(track)
        track.album = '{0} ({1})'.format(track_json['album']['name'],track_json['album']['released'])
        track.track_number = track_json['track-number']
        track.length = track_json['length']
        track.name = track_json['name']
        track.artists = ','.join([artist['name'] for artist in track_json['artists']])
        
    def make_spotify_api_call(self, track):
        url = urllib2.urlopen('{0}{1}'.format(SPOTIFY_LOOKUP_URL, track.spotify_uri))
        track_json = json.load(url)['track']
        return track_json