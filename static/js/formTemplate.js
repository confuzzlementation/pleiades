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
    document.querySelectorAll('fieldset.collapsible').forEach(fieldset => {
        fieldset.classList.remove('collapsed');
        const legend = fieldset.querySelector('legend');
        legend.addEventListener('click', () => {
            fieldset.classList.toggle('collapsed');
        });
    });
});

