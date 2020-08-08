const loc = 'ws://' + window.location.host + window.location.pathname;

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

var updateSocket = new WebSocket(loc + 'updater/');
updateSocket.onmessage = event => {
    $('#board').load('board');
    $('#sidebar').load('sidebar');
};
updateSocket.onclose = event => location.reload(true);

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

function resign() {
    $('#sidebar').load('sidebar/', {'resign': true});
}

$(() => {

    $('#board').load('board');

    $('#sidebar').load('sidebar', () => {

        var messageSocket = new WebSocket(loc + 'messages/');

        messageSocket.onmessage = event => {
            message = JSON.parse(event.data);
            html = '<h6><span class=teal-text>[' + message.user
                + ']</span> ' + message.message + '</h6>';
            $('#messages').append(html);
            var messages = $('#messages')[0];
            messages.scrollTop = messages.scrollHeight - messages.clientHeight;
        };

        $('#message').select();
        $('#message').on('keyup', event => {
            var message = $('#message').val();
            if(event.keyCode == 13 && message != '') {
                messageSocket.send(JSON.stringify({
                    'user': USER,
                    'message': message
                }));
                $('#message').val('');
            }
        });
    });

    $('#copy_code').click(() => {
        navigator.clipboard.writeText(CODE).then(() => {
            M.toast({html: 'Copied Code'});
        });
    });
});