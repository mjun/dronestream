function infoWindowContent(strike) {
    return '<div class="info-window" id="info-window-' + strike["number"] + '">'
        + '<h5>' + moment(strike["date"]).format("MMMM Do YYYY") + '</h5>'
        + '<p>' + strike["narrative"] + '</p>'
        + '</div>';
}

function initMap() {

    var map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(0, 0),
        zoom: 2,
        minZoom: 2
    });

    var infoWindows = [];
    var markers = strike_data.map(function (strike, i) {
        var marker = new google.maps.Marker({
            position: {lat: Number(strike["latitude"]), lng: Number(strike["longitude"])}
        });

        infoWindows[i] = new google.maps.InfoWindow({
            content: infoWindowContent(strike)
        });

        marker.addListener('mouseover', function () {
            infoWindows[i].open(map, marker);
        });

        marker.addListener('mouseout', function () {
            infoWindows[i].close();
        });

        return marker;
    });

    var markerCluster = new MarkerClusterer(map, markers, {
        maxZoom: 20
    });

}