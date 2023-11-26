document.addEventListener("DOMContentLoaded", function() {
    var registerForm = document.getElementById("register-form");
    var formErrorsDiv = document.getElementById("form-errors");

    registerForm.onsubmit = function(event) {
        event.preventDefault();

        // Clear previous errors
        formErrorsDiv.style.display = "none";
        formErrorsDiv.innerHTML = "";

        // Extract form data
        var username = document.getElementById("username").value.trim();
        var email = document.getElementById("email").value.trim();
        var password1 = document.getElementById("password1").value;
        var password2 = document.getElementById("password2").value;

        // Initialize an array to store potential error messages
        var errors = [];

        // Username validation (e.g., non-empty, specific length, character constraints)
        if (!username) errors.push("Username is required.");
        if (username.length < 3 || username.length > 20) errors.push("Username must be between 3 to 20 characters long.");

        // Email validation (basic format check)
        if (!email) errors.push("Email is required.");
        if (!/^\S+@\S+\.\S+$/.test(email)) errors.push("Please enter a valid email address.");

        // Password validation (length, match, and optional complexity)
        if (!password1 || !password2) errors.push("Both password fields are required.");
        if (password1.length < 8 || password1.length > 20) errors.push("Password must be between 8 to 20 characters long.");
        if (password1 !== password2) errors.push("Passwords do not match.");
        // Add more password complexity checks here if needed

        // If there are errors, display them and exit the function
        if (errors.length > 0) {
            formErrorsDiv.innerHTML = errors.map(error => `<div>${error}</div>`).join("");
            formErrorsDiv.style.display = "block";
            return;
        }

        // Perform AJAX request to server
        var formData = new FormData(registerForm);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", registerForm.action, true);
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhr.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken"));

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    window.location.href = "/chatbot";
                } else {
                    formErrorsDiv.textContent = response.error;
                    formErrorsDiv.style.display = "block";
                }
            } else {
                formErrorsDiv.textContent = "An error occurred during registration. Please try again.";
                formErrorsDiv.style.display = "block";
            }
        };

        xhr.onerror = function() {
            formErrorsDiv.textContent = "Network error: Could not connect to the server.";
            formErrorsDiv.style.display = "block";
        };

        xhr.send(formData);
    };
});
