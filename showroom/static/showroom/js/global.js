window.addEventListener('DOMContentLoaded', () => {
    const popup = document.getElementById('popupMessage');
    if (popup) {
        setTimeout(() => {
            popup.style.display = 'none';
        }, 4000);
    }
});