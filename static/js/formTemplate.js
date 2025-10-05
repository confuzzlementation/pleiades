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

document.getElementById('runModelForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // prevent page reload

    const formElements = document.querySelectorAll('#featuresForm input');
    const data = {};
    formElements.forEach(input => {
        if(input.name) data[input.name] = input.value || 0;
    });

    const resultDiv = document.getElementById('modelResult');
    resultDiv.style.opacity = 0; // hide previous result

    try {
        const response = await fetch('{{ url_for("run_model") }}', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        resultDiv.textContent = `Prediction: ${result.prediction}`;
        resultDiv.style.opacity = 1;
        resultDiv.style.transform = 'translateY(0px)';
    } catch (err) {
        resultDiv.textContent = 'Error: Could not get prediction';
        resultDiv.style.opacity = 1;
        resultDiv.style.transform = 'translateY(0px)';
    }
});