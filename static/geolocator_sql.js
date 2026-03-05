document.addEventListener('DOMContentLoaded', function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            // Populate hidden fields
            document.getElementById('latitude').value = position.coords.latitude;
            document.getElementById('longitude').value = position.coords.longitude;
        }, function(error) {
            console.error('Error obtaining location:', error);
        });
    } else {
        alert('Geolocation is not supported by this browser.');
    }
});
