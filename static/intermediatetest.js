// Array of questions and correct answers
var flashcards = [
    { question: "What is `HORSE` in Estonian?", answer: "hoobune" },
    { question: "What is `DOG` in Estonian?", answer: "koer" },
    { question: "What is `FISH` in Estonian ?", answer: "kala" },
    { question: "What is `APPLE` in Estonian ?", answer: "oun" },
    { question: "What is `PEAR` in Estonian ?", answer: "pirn" },
    { question: "What is `PEACH` in Estonian?", answer: "virsik" },
    { question: "What is `BLUE` in Estonian ?", answer: "sinine" },
    { question: "What is `GREEN` in Estonian ?", answer: "roheline" },
    { question: "What is `SILVER` in Estonian ?", answer: "hobedane" },
];

var currentQuestionIndex = 0;

function loadQuestion() {
    var questionElement = document.getElementById("question");
    questionElement.textContent = flashcards[currentQuestionIndex].question;
}

function checkAnswer() {
    var userAnswer = document.getElementById("userAnswer").value;
    var resultElement = document.getElementById("result");

    if (userAnswer.toLowerCase() === flashcards[currentQuestionIndex].answer.toLowerCase()) {
        resultElement.textContent = "Correct!";
        resultElement.classList.add("correct");
    } else {
        resultElement.textContent = "Incorrect. Try again.";
        resultElement.classList.add("incorrect");
        return; // Do not proceed to the next question if the answer is incorrect
    }

    // Clear input field and result message
    document.getElementById("userAnswer").value = "";
    setTimeout(function () {
        resultElement.textContent = "";
        resultElement.classList.remove("correct", "incorrect");
        // Move to the next question or end the flashcards
        currentQuestionIndex++;
        if (currentQuestionIndex < flashcards.length) {
            loadQuestion();
        } else {
            resultElement.textContent = "Congratulations! You have completed all the flashcards.";
        }
    }, 1500); 
}

window.onload = loadQuestion;
