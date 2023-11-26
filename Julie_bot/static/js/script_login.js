document.addEventListener("DOMContentLoaded", function () {
  var loginModal = document.getElementById("loginModal");
  var loginButton = document.getElementById("loginButton");
  var closeButton = document.querySelector(".close-button");
  var loginForm = document.getElementById("login-form");
  var loginErrorDiv = document.getElementById("login-error");

  // Modal button event listeners
  loginButton.onclick = function () {
    loginModal.style.display = "block";
  };

  closeButton.onclick = function () {
    loginModal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == loginModal) {
      loginModal.style.display = "none";
    }
  };

  // Utility function to show error messages
  function showError(message) {
    loginErrorDiv.textContent = message;
    loginErrorDiv.style.display = "block";
  }

  // Form submission event listener
  loginForm.onsubmit = function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Clear any previous error messages
    loginErrorDiv.style.display = "none";
    loginErrorDiv.textContent = "";

    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Validate inputs
    if (!username || !password) {
      showError("Username and password cannot be empty.");
      return; // Exit the function if validation fails
    }

    // Prepare the AJAX request
    var formData = new FormData(loginForm);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", loginForm.action, true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest"); // Indicate that this is an AJAX request
    xhr.setRequestHeader("X-CSRFToken", formData.get("csrfmiddlewaretoken")); // Set CSRF Token

    // Define what happens on successful data submission
    xhr.onload = function () {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        if (response.success) {
          window.location.href = "/chatbot"; // Redirect to chatbot page if successful
        }
      } else if (xhr.status === 400) {
        // If the status code is 400, it's a client-side error, display the error message
        var errorResponse = JSON.parse(xhr.responseText);
        showError(errorResponse.error);
      } else {
        // If another status code is returned, display a generic error message
        showError("An error occurred. Please try again.");
      }
    };

    // Define what happens in case of an error
    xhr.onerror = function () {
      showError("Network error: Could not connect to server."); // Display a network error
    };

    // Send the form data
    xhr.send(formData);
  };
  loginButton.onclick = function () {
    loginModal.style.display = "block";
  };

  closeButton.onclick = function () {
    loginModal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target == loginModal) {
      loginModal.style.display = "none";
    }
  };
  // Gradient animation for buttons
  var buttons = document.querySelectorAll(".btn");
  buttons.forEach(function (btn) {
    btn.onmouseover = function () {
      // Apply a wide gradient background
      this.style.backgroundImage =
        "linear-gradient(to right, #e4b692, #cb8374, #d9b28a, #bfa58a)";
      // Animate the background position
      this.style.backgroundSize = "400% 400%";
      this.style.transition = "background-position 2s ease";
      this.style.backgroundPosition = "right center";
    };

    btn.onmouseout = function () {
      // Reset the gradient background
      this.style.backgroundImage = "";
      this.style.background = "";
      this.style.backgroundSize = "";
      this.style.backgroundPosition = "";
    };
  });
  // Button press animation
  buttons.forEach(function (btn) {
    btn.onmousedown = function () {
      this.style.transform = "scale(0.95)";
    };

    btn.onmouseup = function () {
      this.style.transform = "";
    };

    btn.onmouseleave = function () {
      this.style.transform = "";
    };
  });

  // Close modal on Esc key press
  document.onkeydown = function (evt) {
    evt = evt || window.event;
    var isEscape = false;
    if ("key" in evt) {
      isEscape = evt.key === "Escape" || evt.key === "Esc";
    } else {
      isEscape = evt.keyCode === 27;
    }
    if (isEscape && loginModal.style.display === "block") {
      loginModal.style.opacity = "0";
      loginModal.style.visibility = "hidden";
    }
  };

  // Detect animation end and then hide the modal
  loginModal.addEventListener("transitionend", function (event) {
    if (event.propertyName === "opacity" && loginModal.style.opacity === "0") {
      loginModal.style.display = "none";
    }
  });

  // Display modal with fade-in effect
  loginButton.onclick = function () {
    loginModal.style.display = "block";
    setTimeout(function () {
      loginModal.style.opacity = "1";
      loginModal.style.visibility = "visible";
    }, 10); // Delay to allow display property change to take effect
  };

  // Hide modal with fade-out effect
  closeButton.onclick = function () {
    loginModal.style.opacity = "0";
    loginModal.style.visibility = "hidden";
  };
});
