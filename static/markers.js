// In your main JavaScript file
async function addMarkersFromPython() {
    const response = await fetch('/api/markers');
    const markers = await response.json();

    markers.forEach(markerData => {
        // Use the map library's function to add a marker
        // Example with Google Maps API:
        new google.maps.Marker({
            position: { lat: markerData.lat, lng: markerData.lng },
            map: map, // Assume 'map' is your initialized map instance
            title: markerData.title
        });
        // Example with Leaflet.js:
        // L.marker([markerData.lat, markerData.lng]).addTo(map);
    });
}
// Call the function when the map is ready
// initMap callback or document ready event
