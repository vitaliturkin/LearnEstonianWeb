// result.js
// Assuming 'score' is passed as a query parameter to this page
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const score = parseInt(urlParams.get('score'));

const resultTextElement = document.querySelector('.result-text');
const resultScoreElement = document.querySelector('.result-score');

if (score >= 5) {
    resultTextElement.textContent = 'Congratulations! You are an Estonian expert!';
} else if (score >= 3) {
    resultTextElement.textContent = 'Well done! You have a good knowledge of Estonian.';
} else {
    resultTextElement.textContent = 'Keep learning! You can improve your Estonian skills.';
}

resultScoreElement.textContent = `Your score: ${score}/6`;
