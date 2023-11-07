$(document).ready(function() {
    const chatContainer = $("#chat-container");

    function appendMessage(className, text, isHtml = false) {
        const messageDiv = $("<div>").addClass("message " + className);
        isHtml ? messageDiv.html(text) : messageDiv.text(text);
        chatContainer.append(messageDiv);
        messageDiv.css({ opacity: 0 }).animate({ opacity: 1 }, 500);
        scrollToBottom(chatContainer);
    }

    function scrollToBottom(element) {
        element.scrollTop(element.prop("scrollHeight"));
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    function removeTypingIndicator() {
        $('.typing-indicator').remove();
    }

    function calculateTypingDelay(message) {
        return Math.min(120 * message.length, 3000);
    }

    $(".input-container form").on("submit", function(event) {
        event.preventDefault();
        const messageInput = $('input[name="message"]');
        let messageText = messageInput.val().trim();
    
        if (messageText === "") return;
    
        appendMessage('user', `You: ${messageText}`, false);
        messageInput.val(''); // Clear the input right after appending the message
    
        appendMessage('julie typing-indicator', `Julie: <span class='typing'>typing...</span>`, true);
    
        sendMessage(messageText, messageInput);
    });
    
    function sendMessage(messageText, messageInput) {
        $.ajax({
            type: "POST",
            url: '', // The URL to the server-side script
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie("csrftoken")
            },
            data: { "message": messageText },
            dataType: "json"
        })
        .done(function(data) {
            removeTypingIndicator();
            appendMessage('julie', `Julie: ${data.response}`, true);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.error("There has been a problem with your fetch operation:", textStatus, errorThrown);
            appendMessage('error', 'Sorry, there was an issue with sending your message. Please try again.', false);
        });
    }});    