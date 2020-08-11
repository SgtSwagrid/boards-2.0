from .common.game import *
from .common.handlers import *
from .common.shapes import *


class Pawn(PieceType):

    ID = 0
    TEXTURES = ['chess/white_pawn.png', 'chess/black_pawn.png']

    def move_valid(self, state, piece, x_to, y_to):

        dir = [1, -1][piece.owner_id]
        home = piece.y == [1, 6][piece.owner_id]

        straight = x_to == piece.x and not state.pieces[x_to][y_to]
        normal = straight and y_to - piece.y == dir
        double = straight and y_to - piece.y == 2 * dir and home and \
                 not state.pieces[piece.x][piece.y + dir]

        capture = abs(x_to - piece.x) == 1 and state.pieces[x_to][y_to] and \
                  y_to - piece.y == dir

        return normal or double or capture


class Rook(PieceType):

    ID = 1
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


class ChessMoveHandler(MoveHandler):

    def move_valid(self, state, piece, x_to, y_to):

        return super().move_valid(state, piece, x_to, y_to) and\
            not Chess().check(self.move_piece(state, piece, x_to, y_to))


class PromotionHandler(SelectHandler):

    def show(self, state, event):

        return self.promotion(state) is not None

    def selector(self, state, event):

        promotion = self.promotion(state)

        return PieceSelector([
            Piece(Rook(), state.turn.current_id),
            Piece(Knight(), state.turn.current_id),
            Piece(Bishop(), state.turn.current_id),
            Piece(Queen(), state.turn.current_id)
        ], state, promotion.x, promotion.y, Chess().SHAPE)

    def select(self, state, event, option):

        promotion = self.promotion(state)
        piece = Piece(Chess().PIECES[option.value],
            state.turn.current_id, promotion.x, promotion.y)
        return state.place_piece(piece)

    def promotion(self, state):

        player_id = state.turn.current_id
        row = [7, 0][player_id]
        pawns = state.find_pieces(player_id, Pawn, y=row)
        return pawns[0] if pawns else None


class Chess(Game):

    ID = 2
    NAME = 'Chess'
    SHAPE = Rectangle(8, 8)
    PLAYER_NAMES = ['White', 'Black']

    PIECES = [Pawn(), Rook(), Knight(), Bishop(), Queen(), King()]
    HANDLERS = [ChessMoveHandler(PIECES), PromotionHandler()]

    def on_action(self, state):

        if PromotionHandler().show(state, None): return state
        else: return state.end_turn()

    def initial_piece(self, num_players, x, y):

        if y in (0, 7):
            player_id = 0 if y == 0 else 1

            if x in (0, 7): return Piece(Rook(), player_id)
            elif x in (1, 6): return Piece(Knight(), player_id)
            elif x in (2, 5): return Piece(Bishop(), player_id)
            elif x == 3: return Piece(Queen(), player_id)
            elif x == 4: return Piece(King(), player_id)

        elif y in (1, 6): return Piece(Pawn(), 0 if y == 1 else 1)

    def check(self, state):

        king = state.find_pieces(state.turn.current_id, King)[0]
        next_state = state.end_turn()
        return any(piece.type.move_valid(next_state, piece, king.x, king.y)
            for piece in state.find_pieces(state.turn.next_id))

    #def check_mate(self, state, player):
    #    return not any(self.move_valid(state, piece, x, y)
    #        for x in range(0, self.width)
    #        for y in range(0, self.height)
    #        for piece in state.find_pieces(player_id))


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
