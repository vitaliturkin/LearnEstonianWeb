document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    // Handle login form submission here
    alert("Login Approved!");
});

document.getElementById("guest-btn").addEventListener("click", function() {
    // Handle guest mode button click here
    alert("Guest Mode Choosen!");
});

document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault();
    // Handle signup form submission here
    alert("Sign Up Successful!");
});
