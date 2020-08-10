from .common.game import *
from .common.handlers import *
from .common.shapes import Rectangle


class TicTacToe(Game):

    ID = 1
    NAME = 'Tic Tac Toe'
    SHAPE = Rectangle(3, 3)
    PLAYER_NAMES = ['Naughts', 'Crosses']

    TARGET = 3

    class TicTacToePiece(PieceType):
        ID = 0
        TEXTURES = ['misc/naught.png', 'misc/cross.png']

    PIECES = [TicTacToePiece()]
    HANDLERS = [PlaceHandler(TicTacToePiece())]

    RUN_COLOUR = '#16A085'

    def setup(self, num_players):
        return super().setup(num_players)\
            .set_score(0, 0)\
            .set_score(1, 0)

    def place_valid(self, state, piece):
        return self.SHAPE.in_bounds(piece.x, piece.y) and \
               not state.pieces[piece.x][piece.y]

    def place_piece(self, state, piece):
        state = state.place_piece(piece)
        game_ended = self.has_run(state, piece)
        game_draw = not game_ended and all([state.pieces[x][y]
            for x in range(0, self.SHAPE.width)
            for y in range(0, self.SHAPE.height)])

        return state.end_turn() if not (game_ended or game_draw)\
            else state.end_game(winner_id=state.turn.current_id if not game_draw else -1)

    def colour(self, state, event, x, y):
        col = super().colour(state, event, x, y)

        if state.action:
            last_piece = state.action.piece
            runs = self.runs(state, last_piece)

            if state.outcome.finished and not state.outcome.draw:
                for sub_run in runs:
                    if [x, y] in sub_run:
                        col = self.RUN_COLOUR

        return col

    def has_run(self, state, piece):
        return len(self.runs(state, piece)) > 0

    def runs(self, state, piece):
        directions = [[1, 0], [0, 1], [1, 1], [1, -1]]
        runs = []

        for dir in directions:
            sub_runs = []

            for mult in [-1, 1]:
                for i in range(1, max(self.SHAPE.width, self.SHAPE.height)):
                    x_next = piece.x + mult * i * dir[0]
                    y_next = piece.y + mult * i * dir[1]
                    if state.friendly(x_next, y_next):
                        sub_runs.append([x_next, y_next])
                    else:
                        break

            if len(sub_runs) >= self.TARGET - 1: runs.append(sub_runs)
        return runs