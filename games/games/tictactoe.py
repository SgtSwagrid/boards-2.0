from .common.game import *
from .common.handler import *


class TicTacToe(Game):
    name = "Tic Tac Toe"
    id = 1
    width = 3
    height = 3
    players = 2
    target = 3

    class TicTacToePiece(PieceType):
        id = 0

        def texture(self, owner):
            if owner == 0:
                return 'games/img/misc/naught.png'  # Player 1 is Naughts
            else:
                return 'games/img/misc/cross.png'  # Player 2 is Crosses

    types = [TicTacToePiece()]
    handlers = [PlaceHandler(TicTacToePiece())]

    run_colour = '#16a085'

    def setup(self):
        return super().setup() \
            .set_score(0, 0) \
            .set_score(1, 0)

    def place_valid(self, state, piece):
        return self.in_bounds(piece.x, piece.y) and \
               not state.pieces[piece.x][piece.y]

    def place_piece(self, state, piece):
        state = state.place_piece(piece)
        game_ended = self.has_run(state, piece)

        return state.end_turn() if not game_ended \
            else state.end_game(winner=state.turn.current)

    def colour(self, state, display, x, y):
        col = super().colour(state, display, x, y)

        if state.action:
            last_piece = state.action.piece
            runs = self.runs(state, last_piece)

            if state.outcome.finished and not state.outcome.draw:
                for sub_run in runs:
                    if [x, y] in sub_run:
                        col = self.run_colour

        return col

    def has_run(self, state, piece):
        return len(self.runs(state, piece)) > 0

    def runs(self, state, piece):
        directions = [[1, 0], [0, 1], [1, 1], [1, -1]]
        runs = []

        for dir in directions:
            sub_runs = []

            for mult in [-1, 1]:
                for i in range(1, max(self.width, self.height)):
                    x_next = piece.x + mult * i * dir[0]
                    y_next = piece.y + mult * i * dir[1]
                    if state.friendly(x_next, y_next):
                        sub_runs.append([x_next, y_next])
                    else:
                        break

            if len(sub_runs) >= self.target - 1: runs.append(sub_runs)
        return runs
