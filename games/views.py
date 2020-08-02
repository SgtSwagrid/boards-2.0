from django.shortcuts import render, redirect
import math
from .models import *
from .consumers import *
from .games.common.games import *
from .games.common.input import *

def browse_view(request):

    boards_per_page = 10

    page = int(request.GET['page']) if 'page' in request.GET else 1
    start = (page - 1) * boards_per_page
    end = start + boards_per_page - 1

    boards = BoardModel.boards.all()
    pages = math.ceil(len(boards) / boards_per_page)

    return render(request, 'games/browse.html', {
        'boards': [b.to_dictionary() for b in boards[start:end]],
        'page': page,
        'pages': range(1, pages + 1)
    })

def create_view(request):

    if 'game' in request.GET:

        if not request.user.is_authenticated:
            return redirect('/users/login?next=/games/create?game='
                + request.GET['game'])

        game = games[int(request.GET['game'])]
        board = BoardModel.boards.create(game=game)
        board.join(request.user)

        return redirect('../' + board.code)

    return render(request, 'games/create.html', {
        'games': games.values()
    })

def game_view(request, board_code):

    if not request.user.is_authenticated:
        return redirect('/users/login?next=/games/' + board_code)

    if not BoardModel.boards.filter(code=board_code).exists():
        return render(request, 'games/noboard.html', {})

    board = BoardModel.boards.get(code=board_code)

    return render(request, 'games/game.html', {
        'board': board.to_dictionary(),
        'state': board.state
    })

def board_view(request, board_code):

    board = BoardModel.boards.get(code=board_code)
    state_model = StateModel.states.filter(
        id=int(request.GET['state'])).first()\
        if 'state' in request.GET else board.state
    state = state_model.to_state()

    game = board.game()
    player = board.player(request.user)

    cx, cy = -1, -1
    if 'cx' in request.POST:
        cx, cy = int(request.POST['cx']), int(request.POST['cy'])

    sx, sy = -1, -1
    if 'sx' in request.POST:
        sx, sy = int(request.POST['sx']), int(request.POST['sy'])

    display = Display(game.width, game.height)
    if sx != -1: display = display.select(sx, sy)

    current = board.status == 1 and board.current(player)\
        and state_model == board.state

    if cx != -1 and current:
        result, display = game.event(state, display, BoardEvent(cx, cy))
        if result:
            board.set_state(result)
            notify_board(board)
            state = result

    current = board.status == 1 and board.current(player)\
        and state_model == board.state
    display = display.set_current(current)
    display = game.display(state, display)

    return render(request, 'games/board.html', {
        'tiles': reversed(list(map(list, zip(*display.tiles)))),
        'selected': {
            'x': display.selections[0][0]
                if len(display.selections) > 0 else -1,
            'y': display.selections[0][1]
                if len(display.selections) > 0 else -1
        },
        'current': current
    })

def sidebar_view(request, board_code):

    board = BoardModel.boards.get(code=board_code)
    state_model = StateModel.states.filter(
        id=int(request.GET['state'])).first()\
        if 'state' in request.GET else board.state

    if board.status == 0: setup(request, board)

    player = board.player(request.user)
    if board.status == 1 and 'forfeit' in request.POST and player:
        player.concede()
        notify_board(board)

    return render(request, 'games/sidebar.html', {
        'board': board,
        'state': state_model.to_state(),
        'players': [
            {
                'user': player.user,
                'player': player,
                'state': state,
            }
            for player, state in
                zip(board.players(), state_model.player_states())],
        'turn': board.players()[board.state.current],
        'winner': board.players()[board.state.outcome]\
            if board.state.outcome > -1 else None,
        'this_player': board.player(request.user),
        'previous': state_model.previous,
        'next': StateModel.states.filter(previous=state_model).first(),
        'current': board.state
    })

def setup(request, board):

    this_user = request.user
    this_player = board.player(this_user)
    leader = this_player and this_player.leader

    if 'start' in request.POST and leader:
        board.start()
        notify_board(board)

    elif 'cancel' in request.POST and leader:
        board.delete()
        notify_board(board)

    if 'user' in request.POST:

        other_user = User.objects.get(id=request.POST['user'])
        other_player = board.players().filter(user=other_user).first()
        me = this_user == other_user

        if 'join' in request.POST and not other_player and (leader or me):
            board.join(other_user)
            notify_board(board)

        if 'leave' in request.POST and other_player and (leader or me):
            other_player.leave()
            notify_board(board)

        if 'promote' in request.POST and other_player and leader\
                and other_player.order != 0:
            other_player.promote()
            notify_board(board)

        if 'demote' in request.POST and other_player and leader\
                and other_player.order != board.players().count() - 1:
            other_player.demote()
            notify_board(board)

        if 'transfer' in request.POST and other_player and leader:
            other_player.transfer()
            notify_board(board)