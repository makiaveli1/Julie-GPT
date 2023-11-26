document.addEventListener("DOMContentLoaded", function () {
  var loginModal = document.getElementById("loginModal");
  var loginButton = document.getElementById("loginButton");
  var closeButton = document.querySelector(".close-button");

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
