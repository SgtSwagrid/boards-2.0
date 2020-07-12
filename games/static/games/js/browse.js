$(() => {
    $('#goto_board').click(() => {
        location.href = '/games/' + $('#board_code').val();
    });
});