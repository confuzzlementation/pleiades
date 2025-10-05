var popUp = document.getElementById('popUp');

function displayPopup() {
    popUp.classList.add('show');
}

function closePopup() {
    popUp.classList.remove('show');
}

window.onclick = function(event) {
    if (event.target === popUp) {
        closePopup();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('fieldset.collapsible legend').forEach(legend => {
        legend.addEventListener('click', () => {
            const fieldset = legend.parentElement;
            fieldset.classList.toggle('collapsed');
        });
    });
});

