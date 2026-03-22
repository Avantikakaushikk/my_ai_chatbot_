const userId = "user123";

async function sendMessage() {
    const input = document.getElementById("message");
    const msg = input.value;
    input.value = "";

    addMessage(msg, "user");

    const response = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message: msg })
    });

    const data = await response.json();
    addMessage(data.response, "bot");
}

function addMessage(text, cls) {
    const box = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = cls;
    div.innerText = text;
    box.appendChild(div);
}
addMessage("Typing...", "bot");