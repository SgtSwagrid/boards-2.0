class State:

    def __init__(self, game=None, players=None, pieces=None, turn=None,
            outcome=None, previous=None, changes=-1, state=None):

        self.game = game if game else state.game
        self.players = players if players else state.players
        self.pieces = pieces if pieces else state.pieces
        self.turn = turn if turn else state.turn
        self.outcome = outcome if outcome else state.outcome
        self.changes = changes if changes != -1 else state.changes if state else set()
        self.previous = previous if previous else\
            (state.previous if state else None)

        self.pieces_by_player = {player.order:
            [piece for col in self.pieces for piece in col
                if piece and piece.owner == player.order]
            for player in self.players}

    def end_stage(self, skip=1):
        return State(state=self,
            turn=Turn(turn=self.turn,
                stage=self.turn.stage + skip))

    def end_turn(self, skip=1):
        return State(state=self,
            turn=Turn(turn=self.turn,
                current=(self.turn.current + skip) % len(self.players),
                stage=0,
                ply=self.turn.ply + 1))

    def end_game(self, winner=None):
        return State(state=self,
            outcome=Outcome(outcome=self.outcome,
                finished=True,
                winner=winner,
                draw=not winner))

    def set_piece(self, piece, x, y):
        return State(state=self,
            pieces=[[piece if x == xx and y == yy else self.pieces[xx][yy]
                for yy in range(0, self.game.height)]
                    for xx in range(0, self.game.width)])\
            .set_changed(x, y)

    def place_piece(self, piece):
        return self.set_piece(piece, piece.x, piece.y)\
            if piece else self

    def move_piece(self, piece, x_to, y_to):
        return self.remove_piece(piece)\
                   .place_piece(Piece(piece=piece, x=x_to, y=y_to))

    def remove_piece(self, piece):
        return self.set_piece(None, piece.x, piece.y)

    def exists(self, x, y):
        return self.game.in_bounds(x, y) and self.pieces[x][y]

    def friendly(self, x, y):
        return self.exists(x, y) and\
               self.pieces[x][y].owner == self.turn.current

    def enemy(self, x, y):
        return self.exists(x, y) and\
               self.pieces[x][y].owner != self.turn.current

    def set_score(self, player, score):
        return State(state=self,
            players=[p if p.order != player else
                PlayerState(player=p, score=score) for p in self.players])

    def add_score(self, player, score):
        return self.set_score(player, self.players[player].score + score)

    def set_changed(self, x, y):
        return State(state=self, changes=self.changes | {(x, y)})

    def clear_changes(self):
        return State(state=self, changes=set())

    def changed(self, x, y):
        return any(c == (x, y) for c in self.changes)

class PlayerState:

    def __init__(self, order=-1, score=-1, player=None):
        self.order = order if order != -1 else player.order
        self.score = score if score != -1 else player.score

class Piece:

    def __init__(self, type=None, owner=-1, x=-1, y=-1, piece=None):
        self.type = type if type else piece.type
        self.owner = owner if owner != -1 else piece.owner
        self.x = x if x != -1 else piece.x
        self.y = y if y != -1 else piece.y

class Turn:

    def __init__(self, current=-1, stage=-1, ply=-1, turn=None):
        self.current = current if current != -1 else turn.current
        self.stage = stage if stage != -1 else turn.stage
        self.ply = ply if ply != -1 else turn.ply

class Outcome:

    def __init__(self, finished=-1, winner=-1, draw=-1, outcome=None):
        self.finished = finished if finished != -1 else outcome.finished
        self.winner = winner if winner != -1 else outcome.winner
        self.draw = draw if draw != -1 else outcome.draw