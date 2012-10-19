var music = {

	spotifySearch: function(pageNumber) {
		$.getJSON('http://ws.spotify.com/search/1/track.json?page='+pageNumber+'&q='+$('#spotify_search_form_query').val(), function(data) {
			music.clearSearchResults();
			var info = data['info'];
			var numberOfResults = info['num_results'];
			var offset = info['offset'];
			var limit = info['limit'];
			var tracks = data['tracks'];
			var html="";
			$.each(tracks, function(key, track) {
				var trackData = "";
				var name = track['name'];
				var albumName = track['album']['name'];
				var albumReleaseDate = track['album']['released'];
				var spotifyUri  = track['href'];
					
				var artistsNames = new Array();
				$(track['artists']).each(function(index, value){artistsNames[index] = (value['name']);});
				
				trackData += '<td>'+name+'</td>';
				trackData += '<td>'+artistsNames.join(',')+'</td>';
				trackData += '<td>'+albumName+" ("+albumReleaseDate+')</td>';
				trackData += '<td width="50"><button class="spotify_search_choose_buttons btn btn-primary" name="'+spotifyUri+'"><i class="icon-ok icon-white" /></button></td>';
				
				
				html += '<tr height="18">'+trackData+'</tr>';
			});
			$('#spotify_search_results').html(html);
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
		$('#spotify_search_results').html("");
		$('#spotify_search_results_pagination').html('<div class="pagination"><ul></ul></div>');
		return false;
	},
	populateAndSubmitSongthreadForm: function (inputElement) {
		spotifyUri = $(inputElement).attr("name");
		$('#id_spotify_uri').attr("value", spotifyUri);
		$('#songthread_create_form').submit();
		return false;
	}
	
};

var comment = {
	addReplyToComment: function(inputElement) {
		$('#input_content').val("@"+$(inputElement).parent().attr("username")+"\n");
		$('input[name="in_reply_to"]').val($(inputElement).parent().attr("comment_id"));
		$('#input_content').focus();
		$('html, body').animate({
		    scrollTop: $("#comments_header").offset().top
		}, 500);
	}
}

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
	$('.spotify_search_choose_buttons').live('click', function(event) {return music.populateAndSubmitSongthreadForm(event.target)});
	$('#spotify_search_form_search').bind('click', function() {return music.spotifySearch(1)});
	$('#spotify_search_form_clear').bind('click', function() {return music.clearSearchResults()});
	$('.comment_reply_buttons').bind('click', function(event) {event.preventDefault();return comment.addReplyToComment(event.target)});
	
	if( ! $('#songthread_canvas').tagcanvas({
		textFont: "Arial",
	    textColour : 'black',
	    outlineThickness : 1,
	    maxSpeed : 0.03,
	    initial: [0.1,0.1],
	    depth : 0.75,
	    dragControl: true
	    }, 'songthread_tags')) {
	    $('#songthread_canvas_container').hide();
	   }
	
  audiojs.events.ready(function() {
    var as = audiojs.createAll();
  });
});
