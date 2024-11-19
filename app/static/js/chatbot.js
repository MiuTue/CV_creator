document.getElementById("send-btn").addEventListener("click", function () {
    const input = document.getElementById("chat-input").value;
    const chatWindow = document.getElementById("chat-window");
    const response = document.createElement("p");
    response.innerText = "Chatbot: Let me assist you with " + input;
    chatWindow.appendChild(response);
    document.getElementById("chat-input").value = "";
});
