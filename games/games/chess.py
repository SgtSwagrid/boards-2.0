from .common.game import *
from .common.shapes import *
from .common.handlers import *


class Chess(Game):

    ID = 2
    NAME = 'Chess'
    SHAPE = Rectangle(8, 8)
    PLAYER_NAMES = ['White', 'Black']

    class Pawn(PieceType):

        ID = 0
        TEXTURES = ['chess/white_pawn.png', 'chess/black_pawn.png']

        def move_valid(self, state, piece, x_to, y_to):

            dir = 1 if state.turn.current_id == 0 else -1
            home = piece.y == (1 if state.turn.current_id == 0 else 6)

            straight = x_to == piece.x and not state.pieces[x_to][y_to]
            normal = straight and y_to - piece.y == dir
            double = straight and y_to - piece.y == 2 * dir and home and\
                not state.pieces[piece.x][piece.y + dir]

            capture = abs(x_to - piece.x) == 1 and state.pieces[x_to][y_to] and\
                y_to - piece.y == dir

            return normal or double or capture

    class Rook(PieceType):

        ID = 0
        TEXTURES = ['chess/white_rook.png', 'chess/black_rook.png']

        def move_valid(self, state, piece, x_to, y_to):

            sx, sy = direction(piece.x, piece.y, x_to, y_to)
            d = distance(piece.x, piece.y, x_to, y_to)

            return ((sx == 0) ^ (sy == 0)) and\
                path(piece.x, piece.y, sx, sy, d, state.pieces)

    class Knight(PieceType):

        ID = 2
        TEXTURES = ['chess/white_knight.png', 'chess/black_knight.png']

        def move_valid(self, state, piece, x_to, y_to):

            dx, dy = delta(piece.x, piece.y, x_to, y_to)
            return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

    class Bishop(PieceType):

        ID = 3
        TEXTURES = ['chess/white_bishop.png', 'chess/black_bishop.png']

        def move_valid(self, state, piece, x_to, y_to):

            dx, dy = delta(piece.x, piece.y, x_to, y_to)
            sx, sy = direction(piece.x, piece.y, x_to, y_to)
            d = distance(piece.x, piece.y, x_to, y_to)

            return (abs(dx) == abs(dy)) and\
                   path(piece.x, piece.y, sx, sy, d, state.pieces)

    class Queen(PieceType):

        ID = 4
        TEXTURES = ['chess/white_queen.png', 'chess/black_queen.png']

        def move_valid(self, state, piece, x_to, y_to):

            dx, dy = delta(piece.x, piece.y, x_to, y_to)
            sx, sy = direction(piece.x, piece.y, x_to, y_to)
            d = distance(piece.x, piece.y, x_to, y_to)

            return (((sx == 0) ^ (sy == 0)) or (abs(dx) == abs(dy))) and\
                   path(piece.x, piece.y, sx, sy, d, state.pieces)

    class King(PieceType):

        ID = 5
        TEXTURES = ['chess/white_king.png', 'chess/black_king.png']

        def move_valid(self, state, piece, x_to, y_to):
            return distance(piece.x, piece.y, x_to, y_to) == 1

    PIECES = [Pawn(), Rook(), Knight(), Bishop(), Queen(), King()]
    HANDLERS = [MoveHandler()]

    def piece(self, num_players, x, y):

        if y in (0, 7):
            player_id = 0 if y == 0 else 1

            if x in (0, 7): return Piece(self.Rook(), player_id, x, y)
            elif x in (1, 6): return Piece(self.Knight(), player_id, x, y)
            elif x in (2, 5): return Piece(self.Bishop(), player_id, x, y)
            elif x == 3: return Piece(self.Queen(), player_id, x, y)
            elif x == 4: return Piece(self.King(), player_id, x, y)

        elif y == 1: return Piece(self.Pawn(), 0, x, y)
        elif y == 6: return Piece(self.Pawn(), 1, x, y)

        else: return None

    def move_valid(self, state, piece, x_to, y_to):
        return super().move_valid(state, piece, x_to, y_to) and\
            not self.check(self.move_piece(state, piece, x_to, y_to),
                state.turn.current_id)

    def check(self, state, player_id):
        king = state.find_pieces(player_id, self.King)[0]
        return self.attacking(state, (player_id + 1) % 2, king.x, king.y)

    #def check_mate(self, state, player):
    #    return not any(self.move_valid(state, piece, x, y)
    #        for x in range(0, self.width)
    #        for y in range(0, self.height)
    #        for piece in state.find_pieces(player_id))

    def attacking(self, state, player_id, x, y):
        return any(piece.type.move_valid(state, piece, x, y)
            for piece in state.find_pieces(player_id))

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