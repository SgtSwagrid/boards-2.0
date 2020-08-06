$(() => {
    $('#goto_board').click(() => {
        location.href = '/games/' + $('#board_code').val();
    });

    $('#board_code').on('keyup', event => {
        if(event.keyCode == 13) {
            location.href = '/games/' + $('#board_code').val();
        }
    });
});