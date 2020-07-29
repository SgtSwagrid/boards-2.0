const csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var loc = window.location;

var socket = new WebSocket('ws://' + loc.host + loc.pathname + 'updater/');
socket.onmessage = event => {
    $('#board').load('board');
    $('#sidebar').load('sidebar');
};

function clickBoard(cx=-1, cy=-1, sx=-1, sy=-1) {
    $('#board').load('board/',
        {'cx': cx, 'cy': cy, 'sx': sx, 'sy': sy});
}

function setState(state) {
    $('#board').load('board', 'state=' + state);
    $('#sidebar').load('sidebar', 'state=' + state);
}

function join(user) {
    $('#sidebar').load('sidebar/', {'join': true, 'user': user});
}

function leave(user) {
    $('#sidebar').load('sidebar/', {'leave': true, 'user': user});
}

function transfer(user) {
    $('#sidebar').load('sidebar/', {'transfer': true, 'user': user});
}

function promote(user) {
    $('#sidebar').load('sidebar/', {'promote': true, 'user': user});
}

function demote(user) {
    $('#sidebar').load('sidebar/', {'demote': true, 'user': user});
}

function start() {
    $('#sidebar').load('sidebar/', {'start': true});
}

function cancel() {
    $('#sidebar').load('sidebar/', {'cancel': true});
}

var messageSocket = new WebSocket('ws://' + loc.host + loc.pathname + 'messages/');
messageSocket.onmessage = event => {
    $('#messages')[0].append('<p>' + event.data + '</p>');
};

function sendMessage() {
    messageSocket.send('message: ' + $('#message')[0].value);
}

$(() => {
    $('#board').load('board');
    $('#sidebar').load('sidebar');

    $('#copy_code').click(() => {
        navigator.clipboard.writeText(CODE).then(() => {
            M.toast({html: 'Copied Code'});
        });
    });
    var messages = $('#messages')[0];
    messages.scrollTop = messages.scrollHeight - messages.clientHeight;
    $('#message').select();
});