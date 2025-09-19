// const chatIcon = document.getElementById("chat-icon");
// const chatPopup = document.getElementById("chat-popup");
// const messagesDiv = document.getElementById("chat-messages");
// const input = document.getElementById("messageInput");
// const sendBtn = document.getElementById("sendBtn");

// chatIcon.onclick = () => {
//     chatPopup.style.display = chatPopup.style.display === "flex" ? "none" : "flex";
// };

// let chatSocket = new WebSocket(`wss://${window.location.host}/ws/chat`);

// chatSocket.onmessage = (event) => {
//     const data = JSON.parse(event.data);
//     addMessage(data.answer, "bot");
// };

// function addMessage(text, sender) {
//     const msg = document.createElement("div");
//     msg.className = sender === "user" ? "msg-user" : "msg-bot";
//     msg.textContent = text;
//     messagesDiv.appendChild(msg);
//     messagesDiv.scrollTop = messagesDiv.scrollHeight;
// }

// sendBtn.onclick = () => {
//     const userMsg = input.value.trim();
//     if (!userMsg) return;
//     addMessage(userMsg, "user");
//     input.value = "";
//     chatSocket.send(JSON.stringify({ question: userMsg }));
// };

// input.addEventListener("keypress", (e) => {
//     if (e.key === "Enter") sendBtn.click();
// });
const chatIcon = document.getElementById("chat-icon");
const chatPopup = document.getElementById("chat-popup");
const messagesDiv = document.getElementById("chat-messages");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

let chatSocket;

chatIcon.onclick = () => {
    chatPopup.style.display = chatPopup.style.display === "flex" ? "none" : "flex";

    // Make sure socket is connected when opening chat
    if (!chatSocket || chatSocket.readyState === WebSocket.CLOSED) {
        connectSocket();
    }
};

function connectSocket() {
    chatSocket = new WebSocket(`wss://${window.location.host}/ws/chat`);

    chatSocket.onopen = () => {
        console.log("WebSocket connected");
    };

    chatSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        addMessage(data.answer, "bot");
    };

    chatSocket.onclose = () => {
        console.log("WebSocket closed, reconnecting in 1s...");
        setTimeout(connectSocket, 1000);
    };

    chatSocket.onerror = (err) => {
        console.error("WebSocket error:", err);
        chatSocket.close();
    };
}

function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "msg-user" : "msg-bot";
    msg.textContent = text;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

sendBtn.onclick = () => {
    const userMsg = input.value.trim();
    if (!userMsg) return;
    addMessage(userMsg, "user");
    input.value = "";

    if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
        chatSocket.send(JSON.stringify({ question: userMsg }));
    } else {
        console.log("WebSocket is not open. Waiting to reconnect...");
        setTimeout(() => {
            if (chatSocket.readyState === WebSocket.OPEN) {
                chatSocket.send(JSON.stringify({ question: userMsg }));
            }
        }, 500);
    }
};

input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendBtn.click();
});

// Initial connection
connectSocket();

