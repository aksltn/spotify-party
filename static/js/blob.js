function getRandomBlobShape() {
    const shapeType = Math.random() > 0.5 ? 'polygon' : 'ellipse';
    const points = [];

    if (shapeType == 'polygon') {
        for (let i = 0; i < 5; i++) {
            points.push(`${Math.floor(Math.random() * 101)}% ${Math.floor(Math.random() * 101)}%`);
        }
        return `polygon(${points.join(', ')})`;
    } else {
        const xRad = Math.floor(Math.random() * 50) + 30;
        const yRad = Math.floor(Math.random() * 50) + 30;
        return `ellipse(${xRad}% ${yRad}% at 50% 50%)`;
    }
}

function applyRandomBlobShape() {
    const pfpBlob = document.querySelector('.profile-blob');
    pfpBlob.style.transition = 'clip-path 1s ease-in-out';
    pfpBlob.style.clipPath = getRandomBlobShape();
}

setInterval(applyRandomBlobShape, 3000);