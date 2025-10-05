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

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('slideshow-container');
    const slides = Array.from(container.querySelectorAll('.slide'));
    const total = slides.length;
    if (!total) return;

    const STEP = 90;
    let current = 0;

    function updateArrows() {
        slides.forEach(slide => {
        const left = slide.querySelector('.arrow.left');
        const right = slide.querySelector('.arrow.right');
        if (left) left.classList.toggle('hidden', current === 0);
        if (right) right.classList.toggle('hidden', current === total - 1);
        });
    }

    function goToSlide(index) {
        if (index < 0) index = 0;
        if (index >= total) index = total - 1;
        current = index;
        container.style.transition = 'transform 0.8s ease-in-out';
        container.style.transform = `translateX(-${STEP * current}vw)`;
        updateArrows();
    }

    slides.forEach(slide => {
        if (!slide.querySelector('.arrow.left')) {
        const left = document.createElement('div');
        left.className = 'arrow left';
        left.textContent = '←';
        slide.appendChild(left);
        }
        if (!slide.querySelector('.arrow.right')) {
        const right = document.createElement('div');
        right.className = 'arrow right';
        right.textContent = '→';
        slide.appendChild(right);
        }
    });

    container.querySelectorAll('.arrow.right').forEach(a =>
        a.addEventListener('click', () => goToSlide(current + 1))
    );
    container.querySelectorAll('.arrow.left').forEach(a =>
        a.addEventListener('click', () => goToSlide(current - 1))
    );

    document.addEventListener('keydown', e => {
        if (e.key === 'ArrowRight') goToSlide(current + 1);
        if (e.key === 'ArrowLeft') goToSlide(current - 1);
    });

    let startX = null;
    container.addEventListener('touchstart', e => startX = e.touches[0].clientX, {passive:true});
    container.addEventListener('touchmove', e => {
        if (startX === null) return;
        const dx = e.touches[0].clientX - startX;
        container.style.transition = 'none';
        container.style.transform = `translateX(calc(-${STEP * current}vw + ${dx}px))`;
    }, {passive:true});
    container.addEventListener('touchend', e => {
        container.style.transition = 'transform 0.8s ease-in-out';
        if (startX === null) return;
        const dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 50) {
        if (dx < 0) goToSlide(current + 1);
        else goToSlide(current - 1);
        } else {
        goToSlide(current);
        }
        startX = null;
    });

    goToSlide(0);
});
