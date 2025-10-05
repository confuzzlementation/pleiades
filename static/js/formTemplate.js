var popUp = document.getElementById('popUp');

function displayPopup() {
    popUp.classList.add('show');
}

function closePopup() {
    popUp.classList.remove('show');
}

// Close when clicking outside modal content
window.onclick = function(event) {
    if (event.target === popUp) {
        closePopup();
    }
}
