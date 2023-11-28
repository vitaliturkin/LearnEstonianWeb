const flashcards = document.querySelectorAll('.flashcard');

flashcards.forEach((card, index) => {
    const knowBtn = card.querySelector('.know-btn');
    const dontKnowBtn = card.querySelector('.dont-know-btn');

    let isKnown = false; // Initially, the card is not known

    knowBtn.addEventListener('click', () => {
        isKnown = true;
        updateCardStatus();
    });

    dontKnowBtn.addEventListener('click', () => {
        isKnown = false;
        updateCardStatus();
    });

    // Function to update the card status
    const updateCardStatus = () => {
        if (isKnown) {
            card.classList.remove('not-known'); // Remove the not-known class
            card.classList.add('known'); // Add a class to indicate the card is known
            // You can update backend/database here to store user's choice for this card
        } else {
            card.classList.remove('known'); // Remove the known class
            card.classList.add('not-known'); // Add a class to indicate the card is not known
            // Update backend/database here if needed
        }
    };
});
