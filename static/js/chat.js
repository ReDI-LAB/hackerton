// API CHAT
// const chatIcon = document.getElementById("chat-icon");
// const chatPopup = document.getElementById("chat-popup");
// const messagesDiv = document.getElementById("chat-messages");
// const input = document.getElementById("messageInput");
// const sendBtn = document.getElementById("sendBtn");
// chatIcon.onclick = () => {
//     chatPopup.style.display = chatPopup.style.display === "flex" ? "none" : "flex";
// };
// let chatHistory = [
//     { role: "system", content: "You are a helpful assistant." }
// ];
// function addMessage(text, sender) {
//     const msg = document.createElement("div");
//     msg.className = sender === "user" ? "msg-user" : "msg-bot";
//     msg.textContent = text;
//     messagesDiv.appendChild(msg);
//     messagesDiv.scrollTop = messagesDiv.scrollHeight;
// }
// sendBtn.onclick = async () => {
//     const userMsg = input.value.trim();
//     if (!userMsg) return;
//     addMessage(userMsg, "user");
//     input.value = "";
//     chatHistory.push({ role: "user", content: userMsg });
//     const res = await fetch("/api/chat", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify({ question: userMsg, history: chatHistory })
//     });
//     const data = await res.json();
//     addMessage(data.answer, "bot");
//     chatHistory.push({ role: "assistant", content: data.answer });
// };
// input.addEventListener("keypress", (e) => {
//     if (e.key === "Enter") sendBtn.click();
// });

// WS CHAT
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
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    chatSocket = new WebSocket(`${protocol}://${window.location.host}/ws/chat`);

    // chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat`);

    chatSocket.onopen = () => {
        console.log("WebSocket connected");
    };

    chatSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        addMessage(data.answer, "bot");
    };

    chatSocket.onclose = () => {
        console.log("WebSocket closed, reconnecting in 1s...");
        setTimeout(connectSocket, 100000);
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

