function locateUser() {
    navigator.geolocation.getCurrentPosition(function(position) {
        console.log(position.coords.latitude + ', ' + position.coords.longitude);
    })
}
