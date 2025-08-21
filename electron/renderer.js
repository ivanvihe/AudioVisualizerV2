document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('fullscreen-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      if (window.api && window.api.toggleClone) {
        window.api.toggleClone();
      }
    });
  }
});
