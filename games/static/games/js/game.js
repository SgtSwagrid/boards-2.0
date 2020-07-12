function loadBoard(cx=-1, cy=-1) {
    $('#board').load('board', 'cx=' + cx + '&cy=' + cy + '&sx=' + sx + '&sy=' + sy);
}

function loadSidebar(action='') {
    $('#sidebar').load('sidebar', action);
}

function sendMessage() {
    $(document).on('submit', '#message-form', () => {
        $.get('sidebar?message=' + $('#message')[0].value);
        $('#message')[0].value = '';
    });
}

$(() => {
    $('#board').load('board');
    $('#sidebar').load('sidebar');
    setInterval(() => {
        if(!turn) loadBoard();
        loadSidebar();
    }, 500);

    $('#copy_code').click(() => {
        navigator.clipboard.writeText(CODE).then(() => {
            M.toast({html: 'Copied Code'});
        });
    });
    var messages = $('#messages')[0];
    messages.scrollTop = messages.scrollHeight - messages.clientHeight;
    $('#message').select();
});