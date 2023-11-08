// Ensure that the DOM is ready before executing any code
$(document).ready(function () {
  // Chat-related functionalities
  const chatContainer = $("#chat-container");
  let isUserActive = true;

  // Notify the user with a message
  function notifyUser(message) {
    if (!isUserActive && Notification.permission === "granted") {
      new Notification("New message", {
        body: message,
        icon: "/path/to/icon.png",
      }).onclick = function () {
        window.focus();
      };
    }
  }

  // Request notification permission from the user
  if ("Notification" in window) {
    Notification.requestPermission();
  }

  // Scroll to the bottom of the chat container
  function scrollToBottom(element) {
    element.animate({ scrollTop: element.prop("scrollHeight") }, 500);
  }

  // Display error in the console and the chat
  function displayError(message) {
    console.error(message);
    appendMessage("error", message, false);
  }

  // Append a message to the chat container
  function appendMessage(className, text, isHtml) {
    const messageDiv = $("<div>").addClass("message " + className);
    isHtml ? messageDiv.html(text) : messageDiv.text(text);
    chatContainer.append(messageDiv);
    messageDiv.css({ opacity: 0 }).animate({ opacity: 1 }, 500);
    scrollToBottom(chatContainer);
    notifyUser(text);
  }

  // Update the connection status display
  function updateConnectionStatus() {
    const statusDiv = $("#connection-status");
    if (navigator.onLine) {
      statusDiv.text("Connected").removeClass("offline").addClass("online");
    } else {
      statusDiv.text("Offline").removeClass("online").addClass("offline");
    }
  }

  // Event listeners for online and offline events
  window.addEventListener("online", updateConnectionStatus);
  window.addEventListener("offline", updateConnectionStatus);

  // Remove the typing indicator
  function removeTypingIndicator() {
    $(".typing-indicator").remove();
  }

  // Calculate the delay before showing the typing indicator
  function calculateTypingDelay(message) {
    return Math.min(120 * message.length, 3000);
  }

  // Handling form submission
  $(".input-container form").on("submit", function (event) {
    event.preventDefault();
    const messageInput = $('input[name="message"]');
    let messageText = messageInput.val().trim();
    if (messageText === "") return;
    appendMessage("user", `You: ${messageText}`, false);
    messageInput.val("");
    appendMessage("typing-indicator", `Typing...`, false);
    setTimeout(() => {
      sendMessage(messageText);
    }, calculateTypingDelay(messageText));
  });

  // Send the message to the server
  function sendMessage(messageText) {
    $.ajax({
      type: "POST",
      url: "", // The URL will be the endpoint for message submission on your server
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      data: { message: messageText },
      dataType: "json",
    })
      .done(function (data) {
        removeTypingIndicator();
        appendMessage("reply", data.response, false);
      })
      .fail(function () {
        displayError(
          "Sorry, there was an issue with sending your message. Please try again."
        );
      });
  }

  // Retrieve a cookie value by name
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    return parts.length === 2 ? parts.pop().split(";").shift() : null;
  }

  // Window focus and blur events to track user activity
  $(window)
    .focus(function () {
      isUserActive = true;
    })
    .blur(function () {
      isUserActive = false;
    });

  // Initial call to update the connection status
  updateConnectionStatus();

  // Profile-related functionalities

  // Open profile popup
  $(".profile-btn").on("click", function () {
    // changed to class selector
    $("#profile-popup").fadeIn();
  });

  // Close profile popup
  $("#close-popup-btn").on("click", function () {
    $("#profile-popup").fadeOut();
  });

  // Validate and submit the profile form
  $("#profile-form").on("submit", function (event) {
    event.preventDefault();
    if (validateProfileForm()) {
      let formData = new FormData(this);
      $.ajax({
        type: "POST",
        url: "/update-profile", // Replace with your actual server endpoint
        data: formData,
        contentType: false,
        processData: false,
        dataType: "json",
        success: function (data) {
          if (data.success) {
            $("#profile-popup").fadeOut();
            alert("Profile updated successfully.");
          } else {
            alert("Error updating profile: " + data.message);
          }
        },
        error: function () {
          alert("Network error: Could not update profile.");
        },
      });
    } else {
      alert("Please fill in all required fields.");
    }
  });

  // Profile form validation
  function validateProfileForm() {
    // Implement actual validation logic here
    return true; // Placeholder
  }
});
