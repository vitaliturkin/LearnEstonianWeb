// Array of questions and correct answers
var flashcards = [
    { question: "What is `Boat` in Estonian?", answer: "paat" },
    { question: "What is `BUS` in Estonian?", answer: "buss" },
    { question: "What is `TRUCK` in Estonian ?", answer: "veoauto" },
    { question: "What is `CHAIR` in Estonian ?", answer: "tool" },
    { question: "What is `STEPS` in Estonian ?", answer: "trepp" },
    { question: "What is `WARDROBE` in Estonian?", answer: "riidekapp" },
    { question: "What is `Cold` in Estonian ?", answer: "kulm" },
    { question: "What is `LIGHTNING` in Estonian ?", answer: "valk" },
    { question: "What is `SUNNY` in Estonian ?", answer: "paikseline" },
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
    }, 1500); // Wait for 1.5 seconds before clearing the result message and moving to the next question
}

// Load the first question when the page loads
window.onload = loadQuestion;
