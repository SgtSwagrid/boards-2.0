from .common.game import *
from .common.handler import *


class Amazons(Game):
    name = "Amazons"
    id = 6
    width = 10
    height = 10
    players = 2

    class AmazonPiece(PieceType):
        id = 0

        # White is player 1, black player 2
        def texture(self, owner):
            if owner == 0:
                return 'games/img/chess/white_queen.png'
            else:
                return 'games/img/chess/black_queen.png'

        def move_valid(self, state, piece, x_to, y_to):
            return state.turn.stage == 0 and \
                not state.pieces[piece.x][piece.y] and \
                is_queen_move(state, piece, x_to, y_to)

        def move_piece(self, state, piece, x_to, y_to):
            return state \
                .move_piece(piece, x_to, y_to) \
                .state.end_stage()

    class ArrowPiece(PieceType):
        id = 1

        def texture(self, owner):
            if owner == 0:
                return 'games/img/chess/white_pawn.png'
            else:
                return 'games/img/chess/black_pawn.png'

        def place_valid(self, state, piece):
            if len(state.changes) == 0: return False
            x_from, y_from = state.changes[-1]

            queen = Piece(self, state.turn.current, x_from, y_from)

            return state.turn.stage == 1 and \
                not state.pieces[piece.x][piece.y] and \
                is_queen_move(state, queen, piece.x, piece.y)

        def place_piece(self, state, piece):
            return state \
                .place_piece(self, state.turn.current, piece.x, piece.y) \
                .end_turn()

    types = [AmazonPiece(), ArrowPiece()]
    handlers = [MoveHandler(), PlaceHandler(ArrowPiece())]

    def piece(self, x, y):
        # Top and bottom arrangement
        white_queens = [[3, 0], [6, 0], [0, 3], [9, 3]]
        black_queens = [[3, 9], [6, 9], [0, 6], [9, 6]]

        if [x, y] in white_queens:
            return Piece(self.AmazonPiece(), 0, x, y)  # White

        if [x, y] in black_queens:
            return Piece(self.AmazonPiece(), 1, x, y)  # White

        return None


def is_queen_move(state, piece, x_to, y_to):
    dx, dy = delta(piece.x, piece.y, x_to, y_to)
    sx, sy = direction(piece.x, piece.y, x_to, y_to)
    d = distance(piece.x, piece.y, x_to, y_to)
    return (((sx == 0) ^ (sy == 0)) or (abs(dx) == abs(dy))) and \
           path(piece.x, piece.y, sx, sy, d, state.pieces)


def distance(x_from, y_from, x_to, y_to):
    return max(abs(x_to - x_from), abs(y_to - y_from))


def delta(x_from, y_from, x_to, y_to):
    return abs(x_to - x_from), abs(y_to - y_from)


def direction(x_from, y_from, x_to, y_to):
    return (-1 if x_to < x_from else 0 if x_to == x_from else 1), \
            (-1 if y_to < y_from else 0 if y_to == y_from else 1)


def path(x, y, sx, sy, d, pieces):
    return all(map(lambda r: not pieces
    [x + sx * r][y + sy * r], range(1, d)))
