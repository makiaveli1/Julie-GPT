$(document).ready(function () {
  const chatContainer = $("#chat-container");
  let isUserActive = true;
  const $profileModal = $("#profileModal");
  const $toastContainer = $(".toast-container");

  // Function to append toasts to the toast container
  function showToast(message, type = "info") {
    const toastHTML = `<div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">
          ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>`;
    $toastContainer.append(toastHTML);
    $toastContainer.find(".toast").toast("dispose"); // This will clear the previous toasts
    $toastContainer
      .find(".toast")
      .toast({ autohide: true, delay: 6000 })
      .toast("show"); // Then show the new toast
  }

  // Real-time form validation logic
  function validateInput($input) {
    if ($input.val().trim() === "") {
      $input.addClass("is-invalid");
      showToast("Please fill in all required fields.", "danger");
      return false;
    } else {
      $input.removeClass("is-invalid");
      return true;
    }
  }

  // Profile form submission with validation
  $("#profile-form").on("submit", function (event) {
    event.preventDefault();
    let isValid = true;
    $(this)
      .find("input[required], textarea[required]")
      .each(function () {
        isValid &= validateInput($(this));
      });
    if (isValid) {
      submitProfileForm(new FormData(this));
    }
  });

  // Submit profile form to server
  function submitProfileForm(formData) {
    $.ajax({
      type: "POST",
      url: "/update-profile/",
      data: formData,
      contentType: false,
      processData: false,
      dataType: "json",
    })
      .done(function (data) {
        if (data.success) {
          $profileModal.modal("hide");
          showToast("Profile updated successfully.", "success");
        } else {
          showToast("Error updating profile: " + data.message, "danger");
        }
      })
      .fail(function () {
        showToast("Network error: Could not update profile.", "danger");
      });
  }

  // Notification related functions
  function notifyUser(message) {
    if (!isUserActive && Notification.permission === "granted") {
      new Notification("New message", {
        body: message,
        icon: "/path/to/icon.png",
      }).onclick = function () {
        window.focus();
      };
    } else {
      showToast(message);
    }
  }

  if ("Notification" in window) {
    Notification.requestPermission();
  }

  // Scroll to bottom of chat
  function scrollToBottom() {
    chatContainer.animate(
      { scrollTop: chatContainer.prop("scrollHeight") },
      500
    );
  }

  // Helper functions for chat UI
  function appendMessage(className, text, isHtml) {
    const messageDiv = $("<div>").addClass("message " + className);
    isHtml ? messageDiv.html(text) : messageDiv.text(text);
    chatContainer.append(messageDiv);
    messageDiv.css({ opacity: 0 }).animate({ opacity: 1 }, 500);
    scrollToBottom();
  }

  // Connection status
  function updateConnectionStatus() {
    if (navigator.onLine) {
      showToast("Connected", "success");
    } else {
      showToast("Offline", "danger");
    }
  }

  // Typing indicator
  function removeTypingIndicator() {
    $(".typing-indicator").remove();
  }

  function calculateTypingDelay(message) {
    return Math.min(120 * message.length, 3000);
  }

  // Chat message submission
  $(".input-container form").on("submit", function (event) {
    event.preventDefault();
    const messageInput = $('input[name="message"]');
    let messageText = messageInput.val().trim();
    if (messageText === "") return;
    appendMessage("user-message", `You: ${messageText}`);
    messageInput.val("");
    setTimeout(() => {
      sendMessage(messageText);
    }, calculateTypingDelay(messageText));
  });

  // Send message to server
  function sendMessage(messageText) {
    console.log("Sending message:", messageText); // Log the message being sent

    $.ajax({
      type: "POST",
      url: "",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      data: { message: messageText },
      dataType: "json",
    })
      .done(function (data) {
        console.log("Received response:", data); // Log the response from the server
        removeTypingIndicator();
        appendMessage("chatbot-message", data.response);
      })
      .fail(function (jqXHR, textStatus) {
        console.log("Failed to send message:", textStatus); // Log any failure in sending
        showToast(
          "Sorry, there was an issue with sending your message. Please try again.",
          "danger"
        );
      });
  }

  // Cookie retrieval
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  }

  // Focus and blur events for user activity
  $(window)
    .focus(function () {
      isUserActive = true;
    })
    .blur(function () {
      isUserActive = false;
    });

  // Initial connection status update
  updateConnectionStatus();

  // Modal and toast initialization
  $profileModal.modal({ show: false });
  $(".toast").toast({ autohide: true });
});
