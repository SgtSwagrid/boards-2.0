from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .games.games import games

def browse_view(request):

    boards = Board.boards.all()#.filter(state__outcome=-1)

    return render(request, 'games/browse.html', {
        'boards': map(lambda b: b.to_dictionary(), boards)
    })

def create_view(request):

    if 'game' in request.GET and request.user.is_authenticated:

        game_id = int(request.GET['game'])
        board = Board.boards.create(game_id=game_id)
        Player.objects.create(user=request.user, board=board,
                              order=1, leader=True)

        return redirect('../' + board.code)

    return render(request, 'games/create.html', {
        'games': games.values()
    })

def game_view(request, board_code):

    if not Board.boards.filter(code=board_code).exists():
        return render(request, 'games/noboard.html', {})

    if not request.user.is_authenticated:
        return redirect('/users/login?next=/games/' + board_code)

    board = Board.boards.get(code=board_code)

    if board.stage == 0: setup(request, board)

    if 'message' in request.POST and request.user.is_authenticated:
        Message.objects.create(
            user=request.user,
            message=request.POST['message'],
            board=board)

    return render(request, 'games/game.html', {
        'board': board.to_dictionary(),
        'state': board.state,
        'users': board.users(),
        'this_player': board.player(request.user)
    })

def board_view(request, board_code):

    board = Board.boards.get(code=board_code)
    game = board.game()
    player = board.player(request.user)

    cx, cy = (int(request.GET['cx']), int(request.GET['cy']))\
        if 'cx' in request.GET else (-1, -1)
    sx, sy = (int(request.GET['sx']), int(request.GET['sy']))\
        if 'sx' in request.GET else (-1, -1)

    if cx != -1 and board.current(player):
        if sx != -1 and board.move_piece(sx, sy, cx, cy):
            sx, sy = -1, -1
        elif board.place_piece(0, player.order, cx, cy):
            sx, sy = -1, -1
        elif board.remove_piece(cx, cy):
            sx, sy = -1, -1
        elif (sx != cx or sy != cy) and board.selectable(cx, cy):
            sx, sy = cx, cy
        else: sx, sy = -1, -1
    elif not board.current(player):
        sx, sy = -1, -1

    pieces = board.state.pieces()

    return render(request, 'games/board.html', {
        'tiles': map(lambda y:
            map(lambda x: {
                'x': x,
                'y': y,
                'width': game.scale(x, y)[0],
                'height': game.scale(x, y)[1],
                'background': game.background(x, y)
                    if x != sx or y != sy else game.highlight,
                'piece': pieces[x][y].to_dictionary()
                    if pieces[x][y] else None,
                'selected': x == sx and y == sy
            }, range(0, game.width)),
         range(game.height-1, -1, -1)),
        'selected': {'x': sx, 'y': sy},
        'turn': board.current(player)
    })

def setup(request, board):

    this_user = request.user
    this_player = board.players().filter(user=this_user).first()
    leader = this_player and this_player.leader

    if 'cancel' in request.GET and leader:
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