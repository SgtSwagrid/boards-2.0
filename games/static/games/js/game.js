//const LOC = 'ws://' + window.location.host + window.location.pathname;
const LOC = 'ws://' + window.location.host + '/games/' + CODE + '/';
const PATH = '/games/' + CODE + '/';

const csrftoken = Cookies.get('csrftoken');

const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

const hpadding = 315;
const vpadding = 40;

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

function board(cx, cy, sx, sy) {
    $('#board').load(PATH + 'board/',
        {'cx': cx, 'cy': cy, 'sx': sx, 'sy': sy});
}

function selector(option, tx, ty) {
    $('#board').load(PATH + 'board/',
        {'option': option, 'tx': tx, 'ty': ty});
}

function sidebar(properties) {
    $('#sidebar').load(PATH + 'sidebar/', properties);
}

function state(state) {
    $('#board').load(PATH + 'board/' + state);
    $('#sidebar').load(PATH + 'sidebar/' + state);
}

function redirect(path) {
    window.location = PATH + path;
}

$(() => {

    $('#board').load(PATH + 'board/' + STATE + '/');
    $('#sidebar').load(PATH + 'sidebar/' + STATE + '/');

    var updateSocket = new WebSocket(LOC + 'updater/');
    updateSocket.onmessage = event => {
        $('#board').load(PATH + 'board/');
        $('#sidebar').load(PATH + 'sidebar/');
    };
    updateSocket.onclose = event => location.reload(true);

    var messageSocket = new WebSocket(LOC + 'messages/');

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

    $('#copy_code').click(() => {
        navigator.clipboard.writeText(CODE).then(() => {
            M.toast({html: 'Copied Code'});
        });
    });
});