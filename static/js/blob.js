function applyRandomDelay() {
    const songCards = document.querySelectorAll('.album-art');
    
    songCards.forEach(card => {
        // Generate a random delay between 0s and 2s
        const randomDelay = Math.random() * 3; // Random delay in seconds

        // Apply the random delay as an inline style
        card.style.animationDelay = `${randomDelay}s`;
    });
}

window.onload = function() {
    applyRandomDelay();
}