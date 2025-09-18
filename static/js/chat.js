const chatIcon = document.getElementById("chat-icon");
const chatPopup = document.getElementById("chat-popup");
const messagesDiv = document.getElementById("chat-messages");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

chatIcon.onclick = () => {
    chatPopup.style.display = chatPopup.style.display === "flex" ? "none" : "flex";
};

let chatHistory = [
    { role: "system", content: "You are a helpful assistant." }
];

function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "msg-user" : "msg-bot";
    msg.textContent = text;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

sendBtn.onclick = async () => {
    const userMsg = input.value.trim();
    if (!userMsg) return;
    addMessage(userMsg, "user");
    input.value = "";

    chatHistory.push({ role: "user", content: userMsg });

    const res = await fetch("/api/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ question: userMsg, history: chatHistory })
    });
    const data = await res.json();
    addMessage(data.answer, "bot");

    chatHistory.push({ role: "assistant", content: data.answer });
};

input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendBtn.click();
});