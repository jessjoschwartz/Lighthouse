
        // Note: This example requires that you consent to location sharing when
         // prompted by your browser. If you see a blank space instead of the map, this
         // is probably because you have denied permission for location sharing.

        var map;
        var geocoder = new google.maps.Geocoder();

        function geocodePosition(pos) {
            geocoder.geocode({
                latLng: pos
            }, function (responses) {
                if (responses && responses.length > 0) {
                    updateMarkerAddress(responses[0].formatted_address);
                } else {
                    updateMarkerAddress('Cannot determine address at this location.');
                }
            });
        }

        // function updateMarkerPosition(latLng) {
        //     document.getElementById('info').innerHTML = [
        //         latLng.lat(),
        //         latLng.lng()
        //     ].join(', ');
        // }

        function updateMarkerAddress(str) {
            document.getElementById('address').innerHTML = str;
        }


        function initialize() {
            var mapOptions = {
                zoom: 16
            };
            var map = new google.maps.Map(document.getElementById('map-canvas'),
                mapOptions);
            var latLng;

            // Try HTML5 geolocation
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    latLng = new google.maps.LatLng(position.coords.latitude,
                        position.coords.longitude);
                    console.log(position.coords)
                    var marker = new google.maps.Marker({
                        map: map,
                        position: latLng,
                        draggable: true,
                        title: 'You are here!.'
                    });


                    // // google.maps.event.addListener(marker, 'drag', function (event) {
                    // //     console.debug('new position is ' + event.latLng.lat() + ' / ' + event.latLng.lng());
                    // // });

                    // google.maps.event.addListener(marker, 'dragend', function (event) {
                    //     console.debug('final position is ' + event.latLng.lat() + ' / ' + event.latLng.lng());
                    // });

                    map.setCenter(latLng);

                    // Update current position info.
                    // updateMarkerPosition(latLng);
                    geocodePosition(latLng);

                    // Add dragging event listeners.
                    google.maps.event.addListener(marker, 'dragstart', function () {
                        updateMarkerAddress('Dragging...');
                    });

                    // google.maps.event.addListener(marker, 'drag', function () {
                    //     updateMarkerPosition(marker.getPosition());
                    // });

                    google.maps.event.addListener(marker, 'dragend', function () {
                        geocodePosition(marker.getPosition());
                    });

                }, function () {
                    handleNoGeolocation(true);
                });

            } else {
                // Browser doesn't support Geolocation
                handleNoGeolocation(false);
            }
        }

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

        google.maps.event.addDomListener(window, 'load', initialize);