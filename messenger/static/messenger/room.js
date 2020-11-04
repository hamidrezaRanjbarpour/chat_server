const roomName = JSON.parse(document.getElementById('room-name').textContent);
const author_username = JSON.parse(document.getElementById('author-username').textContent);
// let user = "{{username}}";
console.log(author_username);
const chatSocket = new ReconnectingWebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
    let content = data.content;

    if (content['command'] === 'fetch_messages') {
        for (let m of content['messages']) {
            let message = m.author + ": " + m.content;
            document.querySelector('#chat-log').value += (message + '\n');
        }

    } else if (content['command'] === 'new_message') {
        let message = content.message.author + ": " + content.message.content;
        console.log(message);
        document.querySelector('#chat-log').value += (message + '\n');
    }

};

chatSocket.onopen = function (e) {
    chatSocket.send(JSON.stringify({
        'command': 'fetch_messages',
    }))
}

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'command': 'new_message',
        'from': author_username
    }));
    messageInputDom.value = '';
};