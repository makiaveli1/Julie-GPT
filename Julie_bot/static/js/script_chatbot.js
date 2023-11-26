$(document).ready(function () {
  $(".edit-btn").on("click", function () {
    let field = $(this).data("field");

    // For full name, handle first and last name fields separately
    if (field === "full-name") {
      let displaySelector = "#display-" + field;
      let firstNameInput = "#user-first-name";
      let lastNameInput = "#user-last-name";

      console.log("Display selector:", displaySelector);
      console.log("First name input selector:", firstNameInput);
      console.log("Last name input selector:", lastNameInput);

      // Toggle visibility of the display and input elements
      $(displaySelector).toggleClass("hidden");
      $(firstNameInput).toggleClass("hidden");
      $(lastNameInput).toggleClass("hidden");

      // Populate the input fields with the current profile data if they're becoming visible
      if (
        !$(firstNameInput).hasClass("hidden") &&
        !$(lastNameInput).hasClass("hidden")
      ) {
        let fullNameParts = $(displaySelector).text().trim().split(" ");
        $(firstNameInput).val(fullNameParts[0]);
        if (fullNameParts.length > 1) {
          $(lastNameInput).val(fullNameParts.slice(1).join(" "));
        }
      }
    } else {
      // Handle other fields normally
      let displaySelector = `#display-${field}`;
      let inputSelector = `#user-${field}`;

      $(displaySelector).toggleClass("hidden");
      $(inputSelector).toggleClass("hidden");

      if (!$(inputSelector).hasClass("hidden")) {
        $(inputSelector).val($(displaySelector).text().trim());
      }
    }
  });
  const chatContainer = $("#chat-container");
  let isUserActive = true;
  const $profileModal = $("#profileModal");
  const $toastContainer = $(".toast-container");

  function generateUniqueId() {
    var uniqueId =
      "msg-" +
      Date.now().toString() +
      "-" +
      Math.random().toString(36).substr(2, 9);
    console.log("Generated ID:", uniqueId);
    return uniqueId;
  }

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
          $("#display-username").text(data.username || "[No username]");
          $("#display-email").text(data.email);
          // Set other profile data
          $("#display-phone").text(data.phone);
          $("#display-bio").text(data.bio);

          // Split full name into first and last names for editing
          let fullNameParts = data.full_name.split(" ");
          $("#user-first-name").val(fullNameParts[0]); // Set first name
          if (fullNameParts.length > 1) {
            $("#user-last-name").val(fullNameParts.slice(1).join(" ")); // Set last name
          }

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
          if (!$(this).hasClass("hidden")) {
            // Changed from 'd-none' to 'hidden'
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

  function updateChatboxAvatar(newAvatarUrl) {
    // Update the user avatar in the chatbox
    $(".fa-user.avatar").replaceWith(
      `<img src="${newAvatarUrl}" alt="User" class="avatar" />`
    );
  }

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
            if (data.profile_picture_url) {
              currentUserProfilePicUrl = data.profile_picture_url;
              updateChatboxAvatar(data.profile_picture_url);
            }
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
        icon: "J/media/images/julie.jpg",
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

  function getCurrentTimestamp() {
    // Get the current time in "HH:MM AM/PM" format
    return new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
  }

  function appendMessage(className, text, isHtml, messageId, timestamp) {
    if ($("#" + messageId).length > 0) {
      return; // If the message with the given ID already exists, don't append it again
    }

    const messageDiv = $("<div>")
      .addClass("message " + className)
      .attr("id", messageId);
    let avatarImg;

    if (className.includes("user-message")) {
      avatarImg = $("<img>", {
        src: currentUserProfilePicUrl, // Ensure this variable is defined and holds the current user's avatar URL
        alt: "User",
        class: "avatar",
      });
    } else if (className.includes("chatbot-message")) {
      avatarImg = $("<img>", {
        src: chatbotAvatarUrl, // Ensure this variable is defined and holds the chatbot's avatar URL
        alt: "Chatbot",
        class: "avatar chatbot-avatar",
      });
    } else {
      avatarImg = $("<img>", {
        src: "/path/to/default/avatar.png", // Replace with your default avatar image path
        alt: "Avatar",
        class: "avatar",
      });
    }

    messageDiv.append(avatarImg);
    const messageTextSpan = $("<span>").addClass("message-text");
    isHtml ? messageTextSpan.html(text) : messageTextSpan.text(text);
    messageDiv.append(messageTextSpan);

    if (timestamp) {
      const timestampSpan = $("<span>").addClass("timestamp").text(timestamp);
      messageDiv.append(timestampSpan);
    }

    $("#chat-container").append(messageDiv);
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
  function showTypingIndicator() {
    const typingIndicatorHtml =
      '<div class="typing-indicator">Julie is typing...</div>';
    $("#chat-container").append(typingIndicatorHtml);
  }

  function removeTypingIndicator() {
    $(".typing-indicator").remove();
  }

  function calculateTypingDelay(message) {
    return Math.min(120 * message.length, 3000);
  }

  function sendMessage(messageText, clientMessageId) {
    const timestamp = getCurrentTimestamp(); // Get the current timestamp for immediate display
    appendMessage(
      "user-message",
      messageText,
      false,
      clientMessageId,
      timestamp
    ); // Append the user message immediately with the current timestamp

    // Clear the input field after appending the message
    $('input[name="message"]').val("");

    showTypingIndicator(); // Show typing indicator after sending user message

    $.ajax({
      type: "POST",
      url: "",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken"), // Ensure you're getting the CSRF token correctly
      },
      data: {
        message: messageText,
        client_message_id: clientMessageId, // Make sure this ID is being passed correctly
      },
      dataType: "json",
    })
      .done(function (data) {
        if (data.status === "success") {
          setTimeout(function () {
            removeTypingIndicator(); // Remove typing indicator
            appendMessage(
              "chatbot-message",
              data.response,
              false,
              data.message_id,
              data.timestamp
            ); // Append chatbot's message
            if (!isUserActive) {
              notifyUser("Chatbot has responded");
            }
          }, calculateTypingDelay(data.response));
        } else {
          showToast(data.message, "warning"); // Handle non-success statuses
        }
      })
      .fail(function (jqXHR, textStatus) {
        showToast(
          "Sorry, there was an issue with sending your message. Please try again.",
          "danger"
        );
      });
  }

  $(".input-container form").on("submit", function (event) {
    event.preventDefault();
    const messageInput = $('input[name="message"]');
    const messageText = messageInput.val().trim();
    if (messageText === "") return;

    const clientMessageId = generateUniqueId();
    sendMessage(messageText, clientMessageId);
    messageInput.val(""); // Clear the input field after sending the message
  });

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
  var confirmDeleteBtn = document.getElementById("confirm-delete-btn");
  confirmDeleteBtn.addEventListener("click", function () {
    var deleteUrl = this.getAttribute("data-delete-url"); // Get the delete URL
    var csrfToken = this.getAttribute("data-csrf-token"); // Get the CSRF token

    $.ajax({
      url: deleteUrl,
      method: "POST",
      data: {
        csrfmiddlewaretoken: csrfToken,
      },
      success: function (response) {
        // Redirect to the login page after deletion
        window.location.href = "/login/"; // Change this to the correct URL if needed
      },
      error: function (xhr, textStatus, errorThrown) {
        // Handle errors here
        console.error("Error deleting account: ", textStatus, errorThrown);
      },
    });
  });
});
