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
            card.classList.remove('not-known'); 
            card.classList.add('known'); 
        } else {
            card.classList.remove('known'); 
            card.classList.add('not-known'); 
        }
    };
});
