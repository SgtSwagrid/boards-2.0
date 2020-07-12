function reload(cx=-1, cy=-1) {
    $('#board').load('board', 'cx=' + cx + '&cy=' + cy + '&sx=' + sx + '&sy=' + sy);
}

$(() => {
    $('#board').load('board');
    setInterval(() => {if(!turn) reload()}, 500);

    $('#copy_code').click(() => {
        navigator.clipboard.writeText(CODE).then(() => {
            M.toast({html: 'Copied Code'});
        });
    });
    var messages = $('#messages')[0];
    messages.scrollTop = messages.scrollHeight - messages.clientHeight;
    $('#message').select();
});

