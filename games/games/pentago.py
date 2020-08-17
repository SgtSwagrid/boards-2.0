from .tictactoe import TicTacToe, TicTacToePiece
from .common.handlers import PlaceHandler, SelectHandler
from .common.shapes import Sections
from .common.display import Option


class PentagoPiece(TicTacToePiece):

    ID = 0
    TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']

    def place_valid(self, state, piece):
        return state.turn.stage == 0


class RotationHandler(SelectHandler):

    QUADRANTS = {
        (1, 1): (0, 0),
        (4, 1): (1, 0),
        (4, 4): (1, 1),
        (1, 4): (0, 1)
    }

    def enabled(self, state, x, y):
        return state.turn.stage == 1 and (x, y) in self.QUADRANTS.keys()

    def options(self, state, x, y):
        return [
            Option(0, 0, ['misc/rotate_clockwise.png']),
            Option(1, 1, ['misc/rotate_anticlockwise.png'])
        ]

    def select(self, state, option, x, y):
        qx, qy = self.QUADRANTS[(x, y)]
        return self.rotate(state, qx, qy, option.value == 0)

    def rotate(self, state, qx, qy, clockwise):

        pieces = state.pieces
        size = state.game.SHAPE.width // 2

        for x in range(0, size):
            for y in range(0, size):

                x_to = size * qx + x
                y_to = size * qy + y

                if clockwise:
                    x_from = size * qx + size - 1 - y
                    y_from = size * qy + x

                else:
                    x_from = size * qx + y
                    y_from = size * qy + size - 1 - x

                if pieces[x_from][y_from]:
                    piece = pieces[x_from][y_from].at(x_to, y_to)
                    state = state.place_piece(piece)

                elif pieces[x_to][y_to]:
                    state = state.remove_piece(pieces[x_to][y_to])

        return state


class Pentago(TicTacToe):

    ID = 12
    NAME = 'Pentago'
    SHAPE = Sections([3, 3], [3, 3])
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.wikipedia.org/wiki/Pentago'

    PIECES = [PentagoPiece()]
    HANDLERS = [PlaceHandler(PentagoPiece(), hints=False), RotationHandler()]

    TARGET = 5

    def on_action(self, state):

        captures = [(player_id, self.all_captures(state, player_id))
            for player_id in range(0, state.num_players)]

        captures = [capture for capture in captures if any(capture[1])]

        for player_id, pieces in captures:
            for piece in pieces:
                state = state.set_piece_mode(piece, 1)

        if len(captures) == 1:
            return state.end_game(captures[0][0])

        elif len(captures) > 1 or (state.turn.stage == 1 and
                state.turn.ply + 1 == self.SHAPE.width * self.SHAPE.height):
            return state.end_game()

        elif state.turn.stage == 0: return state.end_stage()

        else: return state.end_turn()

    def all_captures(self, state, player_id):

        captures = (self.captures(state, state.pieces[x][y])
            for x, y in self.SHAPE.positions()
            if state.friendly(x, y, player_id))

        return {capture for c in captures for capture in c}