particlesJS("particles-js", {
    "particles": {
        "number": { "value": 150, "density": { "enable": true, "value_area": 800 } },
        "color": { "value": "#ffffff" },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.8, "random": true },
        "size": { "value": 2, "random": true },
        "line_linked": { "enable": false },
        "move": { "enable": true, "speed": 0.4, "direction": "none", "out_mode": "out" }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": { "onhover": { "enable": true, "mode": "repulse" }, "onclick": { "enable": true, "mode": "push" }, "resize": true }
    },
    "retina_detect": true
});

function createShootingStar() {
    const star = document.createElement("div");
    star.classList.add("shooting-star");
    star.style.left = Math.random() * window.innerWidth + "px";
    document.body.appendChild(star);
    setTimeout(() => star.remove(), 2000);
}
setInterval(createShootingStar, 4000);