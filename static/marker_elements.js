const markerElements = document.querySelectorAll('.custom-marker');
markerElements.forEach(markerEl => {
  markerEl.addEventListener('click', () => {
    const name = markerEl.dataset.name;
    const info = markerEl.dataset.info;
    console.log(`Clicked marker: ${name}. Details: ${info}`);
    // ... display info window logic ...
  });
});
