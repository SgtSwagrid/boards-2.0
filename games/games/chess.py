from .common.game import *
from .common.handler import *

class Chess(Game):

    name = "Chess"
    id = 2
    width = 8
    height = 8
    players = 2

    class Pawn(PieceType):
        id = 0

        def texture(self, owner):
            if owner == 0: return 'games/img/chess/white_pawn.png'
            else: return 'games/img/chess/black_pawn.png'

        def move_valid(self, state, piece, x_to, y_to):

            dir = 1 if state.turn.current == 0 else -1
            home = piece.y == (1 if state.turn.current == 0 else 6)

            straight = x_to == piece.x and not state.pieces[x_to][y_to]
            normal = straight and y_to - piece.y == dir
            double = straight and y_to - piece.y == 2 * dir and home and\
                not state.pieces[piece.x][piece.y + dir]

            capture = abs(x_to - piece.x) == 1 and state.pieces[x_to][y_to] and\
                      y_to - piece.y == dir

            return normal or double or capture

    class Rook(PieceType):
        id = 1

        def texture(self, owner):
            if owner == 0: return 'games/img/chess/white_rook.png'
            else: return 'games/img/chess/black_rook.png'

        def move_valid(self, state, piece, x_to, y_to):

            sx, sy = direction(piece.x, piece.y, x_to, y_to)
            d = distance(piece.x, piece.y, x_to, y_to)

            return ((sx == 0) ^ (sy == 0)) and\
                   path(piece.x, piece.y, sx, sy, d, state.pieces)

    class Knight(PieceType):
        id = 2

        def texture(self, owner):
            if owner == 0: return 'games/img/chess/white_knight.png'
            else: return 'games/img/chess/black_knight.png'

        def move_valid(self, state, piece, x_to, y_to):

            dx, dy = delta(piece.x, piece.y, x_to, y_to)
            return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

    class Bishop(PieceType):
        id = 3

        def texture(self, owner):
            if owner == 0: return 'games/img/chess/white_bishop.png'
            else: return 'games/img/chess/black_bishop.png'

        def move_valid(self, state, piece, x_to, y_to):

            dx, dy = delta(piece.x, piece.y, x_to, y_to)
            sx, sy = direction(piece.x, piece.y, x_to, y_to)
            d = distance(piece.x, piece.y, x_to, y_to)

            return (abs(dx) == abs(dy)) and\
                   path(piece.x, piece.y, sx, sy, d, state.pieces)

    class Queen(PieceType):
        id = 4

        def texture(self, owner):
            if owner == 0: return 'games/img/chess/white_queen.png'
            else: return 'games/img/chess/black_queen.png'

        def move_valid(self, state, piece, x_to, y_to):

            dx, dy = delta(piece.x, piece.y, x_to, y_to)
            sx, sy = direction(piece.x, piece.y, x_to, y_to)
            d = distance(piece.x, piece.y, x_to, y_to)

            return (((sx == 0) ^ (sy == 0)) or (abs(dx) == abs(dy))) and\
                   path(piece.x, piece.y, sx, sy, d, state.pieces)

    class King(PieceType):
        id = 5

        def texture(self, owner):
            if owner == 0: return 'games/img/chess/white_king.png'
            else: return 'games/img/chess/black_king.png'

        def move_valid(self, state, piece, x_to, y_to):
            return distance(piece.x, piece.y, x_to, y_to) == 1

    types = [Pawn(), Rook(), Knight(), Bishop(), Queen(), King()]

    handlers = [MoveHandler()]

    def piece(self, x, y):

        if y in (0, 7):
            player = 0 if y == 0 else 1

            if x in (0, 7): return Piece(self.Rook(), player, x, y)
            elif x in (1, 6): return Piece(self.Knight(), player, x, y)
            elif x in (2, 5): return Piece(self.Bishop(), player, x, y)
            elif x == 3: return Piece(self.Queen(), player, x, y)
            elif x == 4: return Piece(self.King(), player, x, y)

        elif y == 1: return Piece(self.Pawn(), 0, x, y)
        elif y == 6: return Piece(self.Pawn(), 1, x, y)

        else: return None

def distance(x_from, y_from, x_to, y_to):
    return max(abs(x_to - x_from), abs(y_to - y_from))

def delta(x_from, y_from, x_to, y_to):
    return abs(x_to - x_from), abs(y_to - y_from)

def direction(x_from, y_from, x_to, y_to):
    return (-1 if x_to < x_from else 0 if x_to == x_from else 1),\
           (-1 if y_to < y_from else 0 if y_to == y_from else 1)

def path(x, y, sx, sy, d, pieces):
    return all(map(lambda r: not pieces
        [x + sx * r][y + sy * r], range(1, d)))