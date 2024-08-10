// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA13UcUYVermzwm5XHbN-DkLxkHiav7zXA",
  authDomain: "reverse-turing-test-game.firebaseapp.com",
  projectId: "reverse-turing-test-game",
  storageBucket: "reverse-turing-test-game.appspot.com",
  messagingSenderId: "180613192932",
  appId: "1:180613192932:web:841492ed3ad8d28852a0f1",
  measurementId: "G-G0Q283C3WL"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Reference to Firebase Firestore (or other services if needed)
const db = firebase.firestore();

document.addEventListener('DOMContentLoaded', function () {
    const messagesDiv = document.getElementById('messages');
    const inputField = document.getElementById('input');
    const sendButton = document.querySelector('button');

    // Function to append messages to the chat
    function appendMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to bottom
        console.log("Appended message:", message); // Debug log
    }

    // Function to send a message
    function sendMessage() {
        const message = inputField.value.trim();
        if (!message) return; // Don't send empty messages

        console.log("Sending message:", message); // Debug log

        // Send the message to the server
        fetch('http://localhost:5000/make_move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: 1, message: message }) // Adjust the ID and message structure
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(`You: ${message}`);
            appendMessage(`Server: ${data.response}`);
            inputField.value = '';
        })
        .catch(error => console.error('Error:', error));
    }

    // Add event listener for the send button
    sendButton.addEventListener('click', sendMessage);

    // Optionally handle pressing "Enter" to send a message
    inputField.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent newline in the textarea
            sendMessage();
        }
    });

    // Start the game and get initial message
    fetch('http://localhost:5000/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ npc_count: 3 }) // Adjust npc_count as needed
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(`Game: ${data.message}`);
        appendMessage(`You are Robot ${data.player_imposter_index}, the imposter!`);
    })
    .catch(error => console.error('Error:', error));
});
