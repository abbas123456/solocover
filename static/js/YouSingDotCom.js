var music = {

	spotifySearch: function(pageNumber) {
		$.getJSON('http://ws.spotify.com/search/1/track.json?page='+pageNumber+'&q='+$('#spotify_search_form_query').val(), function(data) {
			music.clearSearchResults();
			var info = data['info'];
			var numberOfResults = info['num_results'];
			var offset = info['offset'];
			var limit = info['limit'];
			var tracks = data['tracks'];
			$.each(tracks, function(key, track) {
				var trackData = "";
				var name = track['name'];
				var albumName = track['album']['name'];
				var albumReleaseDate = track['album']['released'];
				var spotifyUri  = track['href'];
					
				var artistsNames = new Array();
				$(track['artists']).each(function(index, value){artistsNames[index] = (value['name']);});
				
				trackData += '<td>'+(offset+key+1)+'</td>';
				trackData += '<td>'+name+'</td>';
				trackData += '<td>'+artistsNames.join(',')+'</td>';
				trackData += '<td>'+albumName+" ("+albumReleaseDate+')</td>';
				trackData += '<td><button class="spotify_search_choose_buttons btn btn-primary" name="'+spotifyUri+'">Choose</button></td>';
				
				
				$('<tr>'+trackData+'</tr>').insertBefore($('#spotify_search_results').children().last());
			});
			music.addPagination(pageNumber, numberOfResults, limit);
			
		});
		return false;
	},
	addPagination: function(pageNumber, numberOfResults, limit) {
		var numberOfPages = Math.ceil(numberOfResults/limit);
		
		var paginationHtml = '<div class="pagination"><ul>';
		for (i=1;i<=numberOfPages;i++) {
			if (i == pageNumber) {
				paginationHtml += '<li class="active"><a class="spotify_search_pagination_buttons" name="'+i+'" href="#">'+i+'</a></li>'	
			} else {
				paginationHtml += '<li><a class="spotify_search_pagination_buttons" href="#">'+i+'</a></li>'
			}
			
		}
		paginationHtml += '</ul></div>';
		$('#spotify_search_results_pagination').html(paginationHtml);
	},
	clearSearchResults: function() {
		$('#spotify_search_results').html('<tr><td></td><td></td><td></td><td></td><td></td></tr>');
		$('#spotify_search_results_pagination').html("");
		return false;
	},
	populateAndSubmitSongthreadForm: function (spotifyUri) {
		$('#id_spotify_uri').attr("value", spotifyUri);
		$('#songthread_create_form').submit();
		return false;
	}
	
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
	
	$('#spotify_search_form').bind('submit', function() {return music.spotifySearch(1)});
	$('.spotify_search_pagination_buttons').live('click', function(event) {event.preventDefault();return music.spotifySearch($(event.target).html())});
	$('.spotify_search_choose_buttons').live('click', function(event) {return music.populateAndSubmitSongthreadForm($(event.target).attr("name"))});
	$('#spotify_search_form_search').bind('click', function() {return music.spotifySearch(1)});
	$('#spotify_search_form_clear').bind('click', function() {return music.clearSearchResults()});
	
	if( ! $('#songthread_canvas').tagcanvas({
		textFont: null,
	    textColour : '#ffffff',
	    outlineThickness : 1,
	    maxSpeed : 0.03,
	    initial: [0.1,0.1],
	    depth : 0.75,
	    dragControl: true
	    }, 'songthread_tags')) {
	    $('#songthread_canvas_container').hide();
	   }
});
