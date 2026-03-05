var autocomplete;
function initAutocomplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('autocomplete'),
    {types: ['geocode']} // Restrict to address results
  );

  // When user selects address, call fillInAddress
  autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
  var place = autocomplete.getPlace();
  // ... Code to extract components (street_number, route, etc.) ...
}
