const chatIcon = document.getElementById("chat-icon");
const chatPopup = document.getElementById("chat-popup");
const messagesDiv = document.getElementById("chat-messages");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

chatIcon.onclick = () => {
    chatPopup.style.display = chatPopup.style.display === "flex" ? "none" : "flex";
};

let chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat`);

chatSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    addMessage(data.answer, "bot");
};

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
    chatSocket.send(JSON.stringify({ question: userMsg }));
};

input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendBtn.click();
});
