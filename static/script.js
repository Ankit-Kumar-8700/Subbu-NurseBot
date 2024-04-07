// Function to send user messages and receive responses
function sendMessage() {
    var userMessage = document.getElementById("user-input").value;
    appendUserMessage(userMessage);

    // Send user message to server for processing
    fetch('/get_response', {
        method: 'POST',
        body: new URLSearchParams({ 'user_message': userMessage }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        var chatBox = document.getElementById("chat-box");
        appendBotMessage(data.response);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error('Error:', error));

    document.getElementById("user-input").value = '';
}

//Function to send already defined messages
function sendRelatedMessage(msg){
    document.getElementById("user-input").value=msg;
    sendMessage();
}

// Function to append user message to the chat container
function appendUserMessage(message) {
    var chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += '<div class="user-message">' + message + '</div>';
}

// Function to append bot message to the chat container
function appendBotMessage(message) {
    var chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += '<div class="bot-message">' + message + '</div>';
}

//function to clear whole chat
function clearChat() {
    var chatBox = document.getElementById("chat-box");
    chatBox.innerHTML="";
}