document.addEventListener('DOMContentLoaded', function () {
    const chatroomForm = document.getElementById('chatroom-form');
    const messageInput = document.getElementById('message-input');
    const chatroomMessages = document.getElementById('chatroom-messages');

    const roomName = '{{ chatroom.name }}';
    
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const message = data['message'];

        chatroomMessages.innerHTML += '<p>' + message + '</p>';
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    chatroomForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const message = messageInput.value;

        chatSocket.send(JSON.stringify({
            'message': message
        }));

        messageInput.value = '';
    });
});