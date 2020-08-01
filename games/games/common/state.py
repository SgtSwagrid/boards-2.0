import copy

class PlayerState:

    def __init__(self, order, score=0, mode=0):
        self.order = order
        self.score = score
        self.mode = mode

class Piece:

    def __init__(self, type, owner, x, y, mode=0):
        self.type = type
        self.owner = owner
        self.x = x
        self.y = y
        self.mode = mode

class Turn:

    def __init__(self, current=0, stage=0, ply=0, epoch=0):
        self.current = current
        self.stage = stage
        self.ply = ply
        self.epoch = epoch

class Outcome:

    def __init__(self, finished=False, winner=-1, draw=False):
        self.finished = finished
        self.winner = winner
        self.draw = draw

class State:

    def __init__(self,
            game,
            players=None,
            pieces=None,
            turn=Turn(),
            outcome=Outcome(),
            previous=lambda: None,
            changes=[]):

        self.game = game

        self.players = players if players else\
            [PlayerState(i) for i in range(0, game.players)]

        self.pieces = pieces if pieces else\
            [[None] * game.height] * game.width

        self.turn = turn
        self.outcome = outcome
        self.changes = changes
        self.previous = previous

        self.pieces_by_player = {player.order:
            [piece for col in self.pieces for piece in col
                if piece and piece.owner == player.order]
            for player in self.players}

    def end_stage(self, skip=1):
        state = copy.deepcopy(self)
        state.turn.stage += skip
        return state

    def end_turn(self, skip=1):
        state = copy.deepcopy(self)
        state.turn.current = (state.turn.current + skip) % len(state.players)
        state.turn.stage = 0
        state.turn.ply += 1
        return state

    def end_epoch(self, skip=1):
        state = copy.deepcopy(self)
        state.turn.epoch += skip
        return state

    def end_game(self, winner=-1):
        state = copy.deepcopy(self)
        state.outcome.finished = True
        state.outcome.winner = winner
        state.outcome.draw = winner == -1
        return state

    def set_piece_mode(self, piece, mode):
        state = copy.deepcopy(self)
        state.pieces[piece.x][piece.y].mode = mode
        return state

    def set_piece(self, piece, x, y):
        state = copy.deepcopy(self)
        state.pieces[x][y] = piece
        state.changes.append((x, y))
        return state

    def place_piece(self, piece):
        return self.set_piece(piece, piece.x, piece.y)\
            if piece else self

    def move_piece(self, piece, x_to, y_to):
        new_piece = copy.deepcopy(piece)
        new_piece.x = x_to
        new_piece.y = y_to
        return self.remove_piece(piece)\
            .place_piece(new_piece)

    def remove_piece(self, piece):
        return self.set_piece(None, piece.x, piece.y)

    def set_score(self, player, score):
        state = copy.deepcopy(self)
        state.players[player].score = score
        return state

    def add_score(self, player, score):
        total = self.players[player].score + score
        return self.set_score(player, total)

    def set_player_mode(self, player, mode):
        state = copy.deepcopy(self)
        state.players[player].mode = mode
        return state

    def exists(self, x, y):
        return self.game.in_bounds(x, y) and self.pieces[x][y]

    def friendly(self, x, y):
        return self.exists(x, y) and\
            self.pieces[x][y].owner == self.turn.current

    def enemy(self, x, y):
        return self.exists(x, y) and\
            self.pieces[x][y].owner != self.turn.current

    def set_changed(self, x, y):
        state = copy.deepcopy(self)
        state.changes.append((x, y))
        return state

    def clear_changes(self):
        state = copy.deepcopy(self)
        state.changes = []
        return state

    def changed(self, x, y):
        return any(c == (x, y) for c in self.changes)