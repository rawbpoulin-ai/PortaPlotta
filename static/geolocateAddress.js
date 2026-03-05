function geocodeAddress() {
    let address = document.getElementById("address").value;
    let apiKey = '09d330c4f9f94cd6a249e3003faae0ed0c99466'; // Replace with your Google API Key
    let url = `https://maps.googleapis.com{encodeURIComponent(address)}&key=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'OK') {
                let location = data.results[0].geometry.location;
                let lat = location.lat;
                let lng = location.lng;

                // Update hidden form fields
                document.getElementById("lat").value = lat;
                document.getElementById("lng").value = lng;

                // Display results (optional)
                document.getElementById("lat-display").innerText = lat;
                document.getElementById("lng-display").innerText = lng;
                console.log("Lat: " + lat + ", Lng: " + lng);
            } else {
                alert("Geocode was not successful: " + data.status);
            }
        })
        .catch(error => console.error('Error:', error));
}
