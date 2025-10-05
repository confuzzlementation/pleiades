var popUp = document.getElementById('popUp');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function displayPopup(){
    popUp.style.display='block';
    popUp.style.width = 'auto';
}

function closePopup(){
    popUp.style.display='none'
}