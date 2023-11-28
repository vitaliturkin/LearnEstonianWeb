// Array of questions and correct answers
var flashcards = [
    { question: "What is `JUNE` in Estonian?", answer: "juuni" },
    { question: "What is `OCTOBER` in Estonian?", answer: "oktoober" },
    { question: "What is `JANUARY` in Estonian ?", answer: "jaanuar" },
      { question: "What is `FOUR` in Estonian ?", answer: "neli" },
      { question: "What is `ONE` in Estonian ?", answer: "uks" },
      { question: "What is `TEN` in Estonian?", answer: "kumme" },
      { question: "What is `CHERRY` in Estonian ?", answer: "kirss" },
      { question: "What is `WATERMELON` in Estonian ?", answer: "arbuus" },
      { question: "What is `SRAWBERRY` in Estonian ?", answer: "maasikas" },
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
