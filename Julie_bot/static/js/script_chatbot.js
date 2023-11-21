$(document).ready(function () {
  $(".edit-btn").on("click", function () {
    let field = $(this).data("field");
    field = field.replace("user_name", "user-name"); // Specific replacement for the username case
    const displaySelector = `#display-${field}`;
    const inputSelector = `#user-${field.replace("user-", "")}`; // Remove the extra 'user-' prefix

    // Toggle visibility
    if ($(displaySelector).css("display") !== "none") {
      // Populate the input field with the current profile data
      $(inputSelector).val($(displaySelector).text());

      // Hide the display element and show the input element
      $(displaySelector).css("display", "none");
      $(inputSelector).css("display", "block");
    } else {
      // Hide the input element and show the display element
      $(displaySelector).css("display", "block");
      $(inputSelector).css("display", "none");
    }
  });
  const chatContainer = $("#chat-container");
  let isUserActive = true;
  const $profileModal = $("#profileModal");
  const $toastContainer = $(".toast-container");

  // Function to append toasts to the toast container
  function showToast(message, type = "info") {
    try {
      // Clear existing toasts before showing a new one
      $toastContainer.find(".toast").remove();

      const toastHTML = `<div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>`;
      $toastContainer.append(toastHTML);
      // Initialize and show the last toast in the container
      $toastContainer
        .find(".toast")
        .last()
        .toast({ autohide: true, delay: 6000 })
        .toast("show");
    } catch (error) {
      console.error("Error displaying toast message:", error);
    }
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

  // Load Profile Data into Modal
  function loadProfileData() {
    try {
      $.ajax({
        type: "GET",
        url: "get-profile-data/", // URL to fetch profile data
        dataType: "json",
        success: function (data) {
          $("#display-full-name").text(data.full_name);
          $("#display-user-name").text(data.username || "[No username]");
          $("#display-email").text(data.email);
          // Set other profile data
          $("#display-phone").text(data.phone);
          $("#display-bio").text(data.bio);
          // Update profile picture, append a timestamp to the URL to prevent caching
          var imageUrl = data.profile_picture;
          if (imageUrl) {
            var timestamp = new Date().getTime();
            imageUrl += "?t=" + timestamp;
            $("#current-profile-picture").attr("src", imageUrl);
          } else {
            // Set a default image if no profile picture URL is provided
            $("#current-profile-picture").attr(
              "src",
              "/path/to/default/profile/image.png"
            );
          }
          console.log("Received profile data:", data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
          console.error("Error loading profile data:", textStatus, errorThrown);
          showToast(
            `Error loading profile data: ${textStatus} - ${errorThrown}`,
            "danger"
          );
        },
      });
    } catch (error) {
      showToast(
        "An unexpected error occurred while loading profile data.",
        "danger"
      );
    }
  }

  // Open Profile Modal Event
  $profileModal.on("show.bs.modal", function () {
    try {
      loadProfileData();
      // Reset to display mode if modal was previously used
      $(".modal-body p").show();
    } catch (error) {
      showToast(
        "An unexpected error occurred when opening the profile modal.",
        "danger"
      );
    }
  });

  // Profile form submission with validation
  $("#profile-form").on("submit", function (event) {
    event.preventDefault();
    try {
      let isValid = true;
      $(this)
        .find("input[required], textarea[required]")
        .each(function () {
          isValid &= validateInput($(this));
        });
      if (isValid) {
        let formData = new FormData(this);
        // Append editable fields data
        $(".edit-input").each(function () {
          if (!$(this).hasClass("d-none")) {
            formData.append(this.name, $(this).val());
          }
        });
        submitProfileForm(formData);
      }
    } catch (error) {
      showToast(
        "An error occurred while submitting the profile form.",
        "danger"
      );
    }
  });

  // Submit profile form to server
  function submitProfileForm(formData) {
    try {
      $.ajax({
        type: "POST",
        url: "update-profile/",
        data: formData,
        contentType: false,
        processData: false,
        dataType: "json",
        success: function (data) {
          if (data.status === "success") {
            setTimeout(function () {
              $profileModal.modal("hide");
              $(".modal-backdrop").remove();
              $("body").removeClass("modal-open");
            }, 500);
            showToast("Profile updated successfully.", "success");
          } else {
            showToast(`Error updating profile: ${data.message}`, "danger");
          }
        },
        error: function (jqXHR, textStatus, errorThrown) {
          console.log("Error details:", textStatus, errorThrown);
          showToast(
            `Network error: Could not update profile: ${textStatus} - ${errorThrown}`,
            "danger"
          );
        },
      });
    } catch (error) {
      showToast(
        "An unexpected error occurred while updating the profile.",
        "danger"
      );
    }
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
