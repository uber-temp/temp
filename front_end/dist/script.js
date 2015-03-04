var map;
var cur_movie;
var movie_titles = [];
var cur_markers = [];
var locations = [];
var movies = [];

function initialize_map() {
    var mapProp = {
        zoom: 10,
        center: new google.maps.LatLng(37.77, -122.447),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

function reset_markers() {
    for (var i = 0; i < cur_markers.length; i++) {
        cur_markers[i].setMap(null);
    }
    cur_markers = [];
}

function get_movie_from_id(oid) {
    $('#cur-mov').html('');
    reset_markers();
    var temp = movies[parseInt(oid) - 1];
    $(temp).each(function(i, data) {
        add_marker(locations[parseInt(data.id) - 1]);
    });
    $.get('http://54.152.249.227/api/v1/movies/' + oid, function(data, status) {
        cur_movie = data;
        console.log(cur_movie);
        var innerHTML = '<h3>'+cur_movie.title+'('+cur_movie.year+')</h3>';
        innerHTML += '<p>Director:'+cur_movie.director.name+'</p>';
        if(cur_movie.writer.name) {
            innerHTML += '<p>Writer:'+cur_movie.writer.name+'</p>';
        }
        $(cur_movie.actors).each(function(i, actor){
            innerHTML += '<p>Actor:'+actor.name+'</p>';
        });
        $('#cur-mov').html(innerHTML);
    });
}

function add_marker(location) {
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(parseFloat(location.latitude), parseFloat(location.longitude)),
        map: map,
        title: location.name
    });
    cur_markers.push(marker);
}

function select_movie(id) {
    get_movie_from_id(id);
}

$(document).ready(function() {
    initialize_map();
    $.get('http://54.152.249.227/api/v1/movies/', function(data, status) {
        $(data).each(function(i, movie) {
            movies.push(movie['locations']);
            movie_titles.push({'label':movie['title'],'value':movie['id']});
            $('#movie-list').append('<li><a href="#" id=' + movie['id'] + '>' + movie['title'] + '</a></li>');
        });
        $('#movie-list li a').click(function() {
            $('#search').val(this.innerHTML);
            get_movie_from_id(this.attributes.id.value);
            select_movie(this.attributes.id.value, this.innerHTML);
        });

        $('#search').autocomplete({
            delay: 0,
            source: movie_titles,
            select: function(evt, element) {
                select_movie(element.item.value);
            }
        });
        $.get('http://54.152.249.227/api/v1/locations/', function(data) {
            $(data).each(function(i, location) {
                locations.push(location);
            });
        });
    });
});
