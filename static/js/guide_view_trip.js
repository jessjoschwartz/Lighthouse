$(document).ready(function() {
    // Note: This example requires that you consent to location sharing when
    // prompted by your browser. If you see a blank space instead of the map, this
    // is probably because you have denied permission for location sharing.

    // Global variables
    var map, originMarker, travelerMarker, destinationMarker;
    var geocoder = new google.maps.Geocoder();

    //Set up Google Maps JavaScript API v3 Directions Service
    var directionsService = new google.maps.DirectionsService();
    var directionsDisplay = new google.maps.DirectionsRenderer({
        suppressMarkers: false
    });

    // Display the route
    function displayRoute(startingPosition) {
        var origin = startingPosition;
        var $map = $("#map-canvas");
        var travelerCurrentLat = $map.data('traveler-current-lat'),
            travelerCurrentLong = $map.data('traveler-current-long'),
            travelerDestinationLat = $map.data('traveler-destination-lat'),
            travelerDestinationLong = $map.data('traveler-destination-long');

        // Setting up latlng points for route
        var request = {
            origin: origin,
            destination: new google.maps.LatLng(travelerDestinationLat, travelerDestinationLong),
            waypoints: [{
                location: new google.maps.LatLng(travelerCurrentLat, travelerCurrentLong)
            }],
            travelMode: google.maps.DirectionsTravelMode.WALKING
        };

        // Specifies map object for directions display
        directionsDisplay.setMap(map);

        // Runs directions service, shows line on map based on current location and destination
        directionsService.route(request, function(response, status) {
            if (status == google.maps.DirectionsStatus.OK) {

                // if (destinationMarker) {
                //     destinationMarker.setMap(null);
                // }

                // if (travelerMarker) {
                //     travelerMarker.setMap(null);
                // }

                directionsDisplay.setDirections(response);

                // var _routeToTraveler = response.routes[0].legs[0];
                // var _routeToDestination = response.routes[0].legs[1];

                // originMarker.setPosition(_routeToTraveler.start_location);

                // travelerMarker = new google.maps.Marker({
                //     position: _routeToTraveler.end_location,
                //     map: map
                // });

                // destinationMarker = new google.maps.Marker({
                //     position: _routeToDestination.start_location,
                //     map: map
                // });
            }
        });
    }

    // Defines map's properties and markers 
    function initialize() {
        var mapOptions = {
            zoom: 16
        };
        map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);
        var latLng;

        // Try HTML5 geolocation
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                latLng = new google.maps.LatLng(position.coords.latitude,
                    position.coords.longitude);
                console.log(position.coords)
                // originMarker = new google.maps.Marker({
                //     map: map,
                //     position: latLng,
                //     draggable: false,
                // });

                // Sets center of map to detected geolocation.    
                map.setCenter(latLng);

                // Display the route
                displayRoute(latLng);

               // Browser cannot get Geolocation 
            }, function() {
                handleNoGeolocation(true);
            });

        } else {
            // Browser doesn't support Geolocation
            handleNoGeolocation(false);
        }
    }

    // Results if geolocation not supported
    function handleNoGeolocation(errorFlag) {
        if (errorFlag) {
            var content = 'Error: The Geolocation service failed.';
        } else {
            var content = 'Error: Your browser doesn\'t support geolocation.';
        }

        // Default coordinates for unsupported geolocation
        var options = {
            map: map,
            position: new google.maps.LatLng(60, 105),
            content: content
        };

        // Centers map
        map.setCenter(options.position);
    }

    // Google Map appears
    google.maps.event.addDomListener(window, 'load', initialize);
});