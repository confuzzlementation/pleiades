var popUp = document.getElementById('popUp');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        closePopup()
    }
}
//fix this
function displayPopup(){
    popUp.style.display = 'flex';
    popUp.style.width = 'auto';
}

function closePopup(){
    popUp.style.display='none'
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}