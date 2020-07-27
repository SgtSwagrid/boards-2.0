from django.shortcuts import render, redirect

from games.games.common.input import ClickInput, Controller
from .models import *
from games.games.common.games import games

def browse_view(request):

    boards = BoardModel.boards.all()#.filter(state__outcome=-1)

    return render(request, 'games/browse.html', {
        'boards': map(lambda b: b.to_dictionary(), boards)
    })

def create_view(request):

    if 'game' in request.GET and request.user.is_authenticated:

        game = games[int(request.GET['game'])]
        board = BoardModel.boards.create(game=game)
        board.join(request.user)

        return redirect('../' + board.code)

    return render(request, 'games/create.html', {
        'games': games.values()
    })

def game_view(request, board_code):

    if not BoardModel.boards.filter(code=board_code).exists():
        return render(request, 'games/noboard.html', {})

    if not request.user.is_authenticated:
        return redirect('/users/login?next=/games/' + board_code)

    board = BoardModel.boards.get(code=board_code)

    return render(request, 'games/game.html', {
        'board': board.to_dictionary()
    })

def board_view(request, board_code):

    board = BoardModel.boards.get(code=board_code)
    game = board.game()
    player = board.player(request.user)

    cx, cy = (int(request.GET['cx']), int(request.GET['cy']))\
        if 'cx' in request.GET else (-1, -1)
    sx, sy = (int(request.GET['sx']), int(request.GET['sy']))\
        if 'sx' in request.GET else (-1, -1)

    contr = Controller(selected={(sx, sy)} if sx != -1 else {})

    if cx != -1 and board.status == 1 and board.current(player):
        input = ClickInput(cx, cy)
        result, contr = board.input(input, contr)
        sx, sy = -1, -1
        for x, y in contr.selected: sx, sy = x, y

    state = board.state.to_state()

    return render(request, 'games/board.html', {
        'tiles': map(lambda y:
            map(lambda x: {
                'x': x,
                'y': y,
                'width': game.scale(x, y)[0],
                'height': game.scale(x, y)[1],
                'texture': game.texture(state, x, y),
                'background': game.colour(state, x, y, contr),
                'piece': state.pieces[x][y]
                    if state.pieces[x][y] else None,
                'selected': x == sx and y == sy
            }, range(0, game.width)),
         range(game.height - 1, -1, -1)),
        'selected': {'x': sx, 'y': sy},
        'turn': board.current(player)
    })

def sidebar_view(request, board_code):

    board = BoardModel.boards.get(code=board_code)

    if board.status == 0: setup(request, board)

    if 'message' in request.GET and request.user.is_authenticated:
        MessageModel.objects.create(
            user=request.user,
            message=request.GET['message'],
            board=board)

    return render(request, 'games/sidebar.html', {
        'board': board.to_dictionary(),
        'state': board.state,
        'users': board.users(),
        'this_player': board.player(request.user)
    })

def setup(request, board):

    this_user = request.user
    this_player = board.players().filter(user=this_user).first()
    leader = this_player and this_player.leader

    if 'start' in request.GET and leader:
        board.start()
    elif 'cancel' in request.GET and leader:
        board.delete()

    if 'user' in request.GET:

        other_user = User.objects.get(id=request.GET['user'])
        other_player = board.players().filter(user=other_user).first()
        me = this_user == other_user

        if 'join' in request.GET and not other_player and (leader or me):
            board.join(other_user)

        if 'leave' in request.GET and other_player and (leader or me):
            other_player.leave()

        if 'promote' in request.GET and other_player and leader\
                and other_player.order != 1:
            other_player.promote()

        if 'demote' in request.GET and other_player and leader\
                and other_player.order != board.players().count():
            other_player.demote()

        if 'transfer' in request.GET and other_player and leader:
            other_player.transfer()