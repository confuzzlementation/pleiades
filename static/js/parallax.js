let targetX = 0;
let targetY = 0;
let currentX = 0;
let currentY = 0;
let time = 0;

document.addEventListener("mousemove", (e) => {
    targetX = (e.clientX / window.innerWidth - .5);
    targetY = (e.clientY / window.innerHeight - .5);
});

function animate() {
    const ease = 0.05;
    currentX += (targetX - currentX) * ease;
    currentY += (targetY - currentY) * ease;

    const stars = document.getElementById("particles-js");
    time += 0.002;

    const autoX = Math.sin(time) * 0.3;
    const autoY = Math.cos(time) * 0.3;
    const autoRotate = Math.sin(time * 0.5) * 2;

    if (stars) {
        stars.style.transform = `translate3d(${(currentX + autoX) * 20}px, ${(currentY + autoY) * 20}px, 0) rotate(${autoRotate}deg)`;
    }
    
    requestAnimationFrame(animate);
}

animate();
