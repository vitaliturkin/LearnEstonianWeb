function showFeedback(questionNumber, correctAnswerIndex) {
    const selectedAnswer = document.querySelector(`input[name="question_${questionNumber}"]:checked`);
    if (selectedAnswer) {
        const selectedValue = selectedAnswer.value;
        const feedbackDiv = document.getElementById(`feedback_${questionNumber}`);
        if (parseInt(selectedValue) === correctAnswerIndex) {
            feedbackDiv.innerHTML = "Correct!";
            feedbackDiv.style.color = "green";
        } else {
            feedbackDiv.innerHTML = "Wrong!";
            feedbackDiv.style.color = "red";
        }
    }
}

function displayScoreMessage(score) {
    let message = '';
    if (score < 3) {
        message = "Your level is beginner.";
    } else if (score < 5) {
        message = "Your level is intermediate.";
    } else {
        message = "Congratulations! Your level is advanced.";
    }
    alert(message);
}