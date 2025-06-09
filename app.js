const messagesDiv = document.getElementById("messages");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");


// Encryption key (In a real app, generate keys securely)
const secretKey = "my-secret-key";

// Initialize WebSocket connection
const ws = new WebSocket("ws://localhost:3000");

// Handle incoming messages
ws.onmessage = (event) => {
    const encryptedMessage = event.data;

    // Decrypt the message
    const bytes = CryptoJS.AES.decrypt(encryptedMessage, secretKey);
    const decryptedMessage = bytes.toString(CryptoJS.enc.Utf8);

    addMessage(decryptedMessage, false);
};

// Send message to server
sendBtn.addEventListener("click", () => {
    const plainText = messageInput.value;
    if (!plainText.trim()) return;

    // Encrypt the message
    const encryptedMessage = CryptoJS.AES.encrypt(plainText, secretKey).toString();

    // Send encrypted message to the server
    ws.send(encryptedMessage);

    // Display message locally
    addMessage(plainText, true);

    messageInput.value = "";
});

function addMessage(text, isSent) {
    const messageElem = document.createElement("div");
    messageElem.classList.add("message");
    messageElem.classList.add(isSent ? "message-sent" : "message-received");
    messageElem.textContent = text;

    messagesDiv.appendChild(messageElem);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Auto-scroll to bottom
}
