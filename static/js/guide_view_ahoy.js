$(document).ready(function() {
    // Note: This example requires that you consent to location sharing when
    // prompted by your browser. If you see a blank space instead of the map, this
    // is probably because you have denied permission for location sharing.

    // Global variables
    var map, originMarker;
    var geocoder = new google.maps.Geocoder();

    // //Set up Google Maps JavaScript API v3 Directions Service
    // directionsService = new google.maps.DirectionsService();
    // directionsDisplay = new google.maps.DirectionsRenderer({
    //     suppressMarkers: true
    // });

    // Set up Google Maps JavaScript API v3 Place Autocomplete 
    // function autoCompleteSetup() {
    //         var autoSrc = new google.maps.places.Autocomplete($("#locations #currentLocation")[0]);
    //         // var autoDest = new google.maps.places.Autocomplete($("#locations #destination")[0]);
    //    }  autoCompleteSetup Ends

    // Handle a click on the request voyage button
    $('#locations').on('submit', function() {
        $('#guide_current_lat').val(originMarker.position.B);
        $('#guide_current_long').val(originMarker.position.k);
    });
        // var origin = originMarker.getPosition();
        // var destination = $("#locations #destination").val();

        // directionsDisplay.setMap(map);

        // var request = {
        //     origin: origin,
        //     // destination: destination,
        //     provideRouteAlternatives: false,
        //     travelMode: google.maps.DirectionsTravelMode.WALKING
        // };

        // // Runs directions service, shows line on map based on current location and destination
        // directionsService.route(request, function(response, status) {
        //     if (status == google.maps.DirectionsStatus.OK) {

        //         directionsDisplay.setDirections(response);

        //         var _route = response.routes[0].legs[0];

        //         // originMarker = new google.maps.Marker({
        //         //     position: _route.start_location,
        //         //     map: map
        //         // });

        //         originMarker.setPosition(_route.start_location);

        //         // if (destinationMarker) {
        //         //     destinationMarker.setMap(null);
        //         // }
        //         // destinationMarker = new google.maps.Marker({
        //         //     position: _route.end_location,
        //         //     map: map
        //         // });
        //         // console.log(destinationMarker.position);

                // Send location data to the db
                function postGuideLocation() { 
                    var locationData = {
                        guide_current_lat: originMarker.position.B,
                        guide_current_long: originMarker.position.k,
                    };
                    $.post('/guide_view', locationData, function(data) {
                        console.log(data);
                    });
                }
                //     // traveler_destination_lat: destinationMarker.position.B,
                //     // traveler_destination_long: destinationMarker.position.k,
                // });
    //         }
    //     });
    // });

    // Geocodes latlng
    function geocodePosition(pos) {
        geocoder.geocode({
            latLng: pos
        }, function(responses) {
            if (responses && responses.length > 0) {
                updateMarkerAddress(responses[0].formatted_address);
            } else {
                updateMarkerAddress('Cannot determine address at this location.');
            }
        });
    }

    function updateMarkerAddress(str) {
        $("#locations #currentLocation").val(str);
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
                originMarker = new google.maps.Marker({
                    map: map,
                    position: latLng,
                    draggable: false,
                });

                // Sets center of map to detected geolocation.    
                map.setCenter(latLng);

                // Update current position info.
                geocodePosition(latLng);

                // // Add dragging event listener for markers.
                // google.maps.event.addListener(originMarker, 'dragstart', function() {
                //     updateMarkerAddress('Dragging...');
                // });

                // google.maps.event.addListener(originMarker, 'dragend', function() {
                //     geocodePosition(originMarker.getPosition());
                //     // LatLong of first marker
                //     // console.log(originMarker.getPosition())
                // });

            }, function() {
                handleNoGeolocation(true);
            });

        } else {
            // Browser doesn't support Geolocation
            handleNoGeolocation(false);
        }

        // autoCompleteSetup();

    }4

    // Results if geolocation not supported
    function handleNoGeolocation(errorFlag) {
        if (errorFlag) {
            var content = 'Error: The Geolocation service failed.';
        } else {
            var content = 'Error: Your browser doesn\'t support geolocation.';
        }

        var options = {
            map: map,
            position: new google.maps.LatLng(60, 105),
            content: content
        };

        var infowindow = new google.maps.InfoWindow(options);
        map.setCenter(options.position);
    }

    // Makes "Ahoy, I'm ready to walk!" button functional
    // $("input[type=submit]").click(function (){
    //     postRoute();
    // })

    // Google Map appears
    google.maps.event.addDomListener(window, 'load', initialize);
});