from django.shortcuts import render, redirect
from django.http import HttpResponse
import math
from .models import *
from .consumers import *
from .games.common.games import *
from .games.common.events import *


def browse_view(request):

    boards_per_page = 10

    page = int(request.GET['page']) if 'page' in request.GET else 1
    start = (page - 1) * boards_per_page
    end = start + boards_per_page

    boards = BoardModel.boards.all()
    pages = math.ceil(len(boards) / boards_per_page)

    return render(request, 'games/browse.html', {
        'boards': [{
            'board': board,
            'status': status(board, request.user)
         } for board in boards[start:end]],
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

def game_view(request, board_code, state_id):

    if not request.user.is_authenticated:
        return redirect('/users/login?next=/games/' + board_code)

    if not BoardModel.boards.filter(code=board_code).exists():
        return render(request, 'games/game_invalid.html', {})

    board = BoardModel.boards.get(code=board_code)

    if state_id == -1: state_id = board.state.id
    state_model = StateModel.states.get(id=state_id)

    return render(request, 'games/game.html', {
        'board': board,
        'state': state_model
    })

def board_view(request, board_code, state_id):

    if not BoardModel.boards.filter(code=board_code).exists():
        return render(request, 'games/board_deleted.html')

    board = BoardModel.boards.get(code=board_code)
    if state_id == -1: state_id = board.state.id
    state_model = StateModel.states.get(id=state_id)
    state = state_model.get_state()

    game = board.game()
    player = board.player(request.user)

    clicked = None
    if 'cx' in request.POST:
        pos = Vec(int(request.POST['cx']), int(request.POST['cy']))
        if game.SHAPE.in_bounds(pos): clicked = pos

    selected = None
    if 'sx' in request.POST:
        pos = Vec(int(request.POST['sx']), int(request.POST['sy']))
        if game.SHAPE.in_bounds(pos): selected = pos

    target = None
    if 'tx' in request.POST:
        pos = Vec(int(request.POST['tx']), int(request.POST['ty']))
        if game.SHAPE.in_bounds(pos): target = pos

    active = board.status == 1 and board.is_current(player)\
        and state_model == board.state
    player_id = player.order if player else -1

    properties = DisplayProperties([selected] if selected else [])

    if clicked and active:
        event = BoardEvent(properties, player_id, active, clicked)
        result, properties = game.on_event(state, event)

        if result:
            board.set_state(result)
            notify_board(board)
            state = result

    if 'option' in request.POST and active:
        option_id = int(request.POST['option'])
        event = SelectEvent(properties, player_id, active, option_id, target)
        result, properties = game.on_event(state, event)

        if result:
            board.set_state(result)
            notify_board(board)
            state = result

    active = active and board.is_current(player)
    event = RenderEvent(properties, player_id, active)
    display = game.on_render(state, event).scale(800, 800)

    return render(request, 'games/board.html', {
        'display': display,
        'event': event
    })

def sidebar_view(request, board_code, state_id):

    if not BoardModel.boards.filter(code=board_code).exists():
        return HttpResponse('')

    board = BoardModel.boards.filter(code=board_code).get()
    game = board.game()
    if state_id == -1: state_id = board.state.id
    state_model = StateModel.states.get(id=state_id)
    player = board.player(request.user)

    if board.status == 0: setup(request, board)

    if board.status == 1 and 'resign' in request.POST and player:
        player.resign()
        notify_board(board)

    if 'cancel' in request.POST and player and player.leader and board.status != 1:
        board.delete()
        notify_board(board)

    if 'rematch' in request.POST and player and board.status == 2:
        rematch = board.join_rematch(request.user)
        notify_board(board)
        return redirect('/games/' + rematch.code)

    if not BoardModel.boards.filter(code=board_code).exists():
        return HttpResponse('')

    return render(request, 'games/sidebar.html', {
        'board': board,
        'state_model': state_model,
        'state': state_model.get_state(),
        'players': [
            {
                'user': player.user,
                'player': player,
                'state': state,
                'name': game.PLAYER_NAMES[player.order]
            }
            for player, state in
                zip(board.players(), state_model.get_player_states())],
        'turn': board.current(),
        'winner': board.winner(),
        'this_player': board.player(request.user),
        'first': board.first_state(),
        'previous': state_model.previous,
        'next': board.next_state(state_model),
        'current': board.state,
        'status': status(board, request.user)
    })

def rematch_view(request, board_code):

    board = BoardModel.boards.get(code=board_code)
    rematch = board.join_rematch(request.user)
    notify_board(rematch)
    return redirect('/games/' + rematch.code)

def fork_view(request, board_code, state_id):

    board = BoardModel.boards.get(code=board_code)
    state = StateModel.states.get(id=state_id)
    fork = BoardModel.boards.fork(board, state, request.user)
    notify_board(fork)
    return redirect('/games/' + fork.code)

def setup(request, board):

    this_user = request.user
    this_player = board.player(this_user)
    leader = this_player and this_player.leader

    if 'start' in request.POST and leader:
        board.start()
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

def status(board, user):

    player = board.player(user)
    num_players = len(board.players())
    current = board.current()
    winner = board.winner()

    if board.status == 0:

        if num_players < board.min_players():
            return 'Awaiting Players'

        elif player:
            return 'Ready'

        elif num_players >= board.max_players():
            return 'Game Full'

        else: return 'Waiting'

    elif board.status == 1:

        if player == current:
            return 'Your Turn'

        elif current:
            return current.user.username + '\'s Turn'

        else: return '???\'s Turn'

    elif board.status == 2:

        if player == winner:
            return 'You Won'

        elif winner:
            return winner.user.username + ' Won'

        else: return 'Draw'

    else: return 'Invalid'
