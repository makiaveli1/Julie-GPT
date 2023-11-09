$(document).ready(function () {
  const chatContainer = $("#chat-container");
  let isUserActive = true;
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
  if ("Notification" in window) {
    Notification.requestPermission();
  }
  function scrollToBottom(element) {
    element.animate({ scrollTop: element.prop("scrollHeight") }, 500);
  }
  function displayError(message) {
    console.error(message);
    appendMessage("error", message, false);
  }
  function appendMessage(className, text, isHtml) {
    const messageDiv = $("<div>").addClass("message " + className);
    isHtml ? messageDiv.html(text) : messageDiv.text(text);
    chatContainer.append(messageDiv);
    messageDiv.css({ opacity: 0 }).animate({ opacity: 1 }, 500);
    scrollToBottom(chatContainer);
    notifyUser(text);
  }
  function updateConnectionStatus() {
    const statusDiv = $("#connection-status");
    if (navigator.onLine) {
      statusDiv.text("Connected").removeClass("offline").addClass("online");
    } else {
      statusDiv.text("Offline").removeClass("online").addClass("offline");
    }
  }
  window.addEventListener("online", updateConnectionStatus);
  window.addEventListener("offline", updateConnectionStatus);
  function removeTypingIndicator() {
    $(".typing-indicator").remove();
  }
  function calculateTypingDelay(message) {
    return Math.min(120 * message.length, 3000);
  }
  $(".input-container form").on("submit", function (event) {
    event.preventDefault();
    const messageInput = $('input[name="message"]');
    let messageText = messageInput.val().trim();
    if (messageText === "") return;
    appendMessage("user", `You:${messageText}`, false);
    messageInput.val("");
    appendMessage("typing-indicator", `Typing...`, false);
    setTimeout(() => {
      sendMessage(messageText);
    }, calculateTypingDelay(messageText));
  });
  function sendMessage(messageText) {
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
        removeTypingIndicator();
        appendMessage("reply", data.response, false);
      })
      .fail(function () {
        displayError(
          "Sorry,there was an issue with sending your message. Please try again."
        );
      });
  }
  function getCookie(name) {
    const value = `;${document.cookie}`;
    const parts = value.split(`;${name}=`);
    return parts.length === 2 ? parts.pop().split(";").shift() : null;
  }
  $(window)
    .focus(function () {
      isUserActive = true;
    })
    .blur(function () {
      isUserActive = false;
    });
  updateConnectionStatus();
  $(".profile-btn").on("click", function () {
    $("#profile-popup").fadeIn();
  });
  $("#close-popup-btn").on("click", function () {
    $("#profile-popup").fadeOut();
  });
  $("#profile-form").on("submit", function (event) {
    event.preventDefault();
    if (validateProfileForm()) {
      let formData = new FormData(this);
      $.ajax({
        type: "POST",
        url: "/update-profile",
        data: formData,
        contentType: false,
        processData: false,
        dataType: "json",
        success: function (data) {
          if (data.success) {
            $("#profile-popup").fadeOut();
            alert("Profile updated successfully.");
          } else {
            alert("Error updating profile:" + data.message);
          }
        },
        error: function () {
          alert("Network error:Could not update profile.");
        },
      });
    } else {
      alert("Please fill in all required fields.");
    }
  });
  function validateProfileForm() {
    return true;
  }
});
