const clientId = prompt("Digite seu ID de cliente:");

const websocket = new WebSocket(`redis-10133.c60.us-west-1-2.ec2.redns.redis-cloud.com:10133/${clientId}`);

websocket.onmessage = function(event) {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p>${event.data}</p>`;
};


function sendMessage() {
    const messageInput = document.getElementById("message-input");
    const message = messageInput.value;
    if (message.trim() !== "") {
        websocket.send(message);
        messageInput.value = "";
    }
}
