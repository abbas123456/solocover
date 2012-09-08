var music = {
		
		
		
};


$(function() {
	$('#id_spotify_lookup_button').bind('click', function() {
		if ($('#id_spotify_lookup_url').val() == "") {
			alert("Please pase a spotify uri");
			return false;
		}
		$.getJSON('http://ws.spotify.com/lookup/1/.json?uri='+$('#id_spotify_lookup_url').val(), function(data) {
			var track = data['track'];
			$('#id_album').val(track['album']['name']+"-"+track['album']['released']);
			$('#id_track_number').val(track['track-number']);
			$('#id_length').val(track['length']);
			$('#id_name').val(track['name']);
			var artistsNames = new Array();
			$(track['artists']).each(function(index, value){artistsNames[index] = (value['name']);});
			$('#id_artists').val(artistsNames.join(','));
			$('#id_spotify_uri').val(track['href']);
		});
	});
});
