from .common.game import *


class Pawn(PieceType):

    ID = 0
    TEXTURES = ['chess/white_pawn.png', 'chess/black_pawn.png']

    def move_valid(self, state, piece, pos):

        dir = [1, -1][piece.owner_id]
        home = piece.y == [1, 6][piece.owner_id]

        straight = pos.x == piece.pos.x and not state.piece_at(pos)
        normal = straight and pos.y - piece.pos.y == dir
        double = straight and pos.y - piece.pos.y == 2 * dir and home and\
            not state.pieces_at(piece.pos + (0, dir))

        capture = abs(pos.x - piece.x) == 1 and state.piece_at(pos) and\
            pos.y - piece.pos.y == dir

        return normal or double or capture


class Rook(PieceType):

    ID = 1
    TEXTURES = ['chess/white_rook.png', 'chess/black_rook.png']

    def move_valid(self, state, piece, pos):

        dir = piece.pos.direction(pos)
        dist = distance(piece.x, piece.y, x_to, y_to)

        return ((sx == 0) ^ (sy == 0)) and\
            path(piece.x, piece.y, sx, sy, d, state.pieces)


class Knight(PieceType):

    ID = 2
    TEXTURES = ['chess/white_knight.png', 'chess/black_knight.png']

    def move_valid(self, state, piece, pos):

        dx = abs(pos - piece.pos).x)
        dx, dy = delta(piece.x, piece.y, x_to, y_to)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)


class Bishop(PieceType):

    ID = 3
    TEXTURES = ['chess/white_bishop.png', 'chess/black_bishop.png']

    def move_valid(self, state, piece, pos):

        dx, dy = delta(piece.x, piece.y, x_to, y_to)
        sx, sy = direction(piece.x, piece.y, x_to, y_to)
        d = distance(piece.x, piece.y, x_to, y_to)

        return (abs(dx) == abs(dy)) and\
            path(piece.x, piece.y, sx, sy, d, state.pieces)


class Queen(PieceType):

    ID = 4
    TEXTURES = ['chess/white_queen.png', 'chess/black_queen.png']

    def move_valid(self, state, piece, pos):

        dx, dy = delta(piece.x, piece.y, x_to, y_to)
        sx, sy = direction(piece.x, piece.y, x_to, y_to)
        d = distance(piece.x, piece.y, x_to, y_to)

        return (((sx == 0) ^ (sy == 0)) or (abs(dx) == abs(dy))) and\
            path(piece.x, piece.y, sx, sy, d, state.pieces)


class King(PieceType):

    ID = 5
    TEXTURES = ['chess/white_king.png', 'chess/black_king.png']

    def move_valid(self, state, piece, pos):

        return distance(piece.x, piece.y, x_to, y_to) == 1


class ChessMoveHandler(MoveHandler):

    def move_valid(self, state, piece, pos):

        return super().move_valid(state, piece, pos) and\
            not state.game.check(self.move_piece(state, piece, pos)) and\
            not PromotionHandler().promotion(state)

    def move_piece(self, state, piece, pos):

        state = super().move_piece(state, piece, pos)
        return state.set_piece_mode(state.piece_at(pos), 1)


class PromotionHandler(MultiPlaceHandler):

    def enabled(self, state, pos):

        return state.friendly(pos) and\
            isinstance(state.piece_at(pos).type, Pawn) and\
            pos.y == [7, 0][state.turn.current_id]

    def pieces(self, state, pos):
        return [Rook(), Knight(), Bishop(), Queen()]

    def promotion(self, state):

        player_id = state.turn.current_id
        pieces = state.find_pieces(player_id, Pawn(), y=[7, 0][player_id])
        return pieces[0] if any(pieces) else None


class Chess(Game):

    ID = 2
    NAME = 'Chess'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(8, 8)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.wikipedia.org/wiki/Chess'

    PIECES = [Pawn(), Rook(), Knight(), Bishop(), Queen(), King()]

    HANDLERS = [
        ChessMoveHandler(PIECES),
        PromotionHandler(click_to_show=False)
    ]

    def on_action(self, state):

        if PromotionHandler().promotion(state): return state
        else: return state.end_turn()

    def initial_piece(self, num_players, pos):

        if pos.y in (0, 7):
            player_id = 0 if pos.y == 0 else 1

            if pos.x in (0, 7): return Piece(Rook(), player_id)
            elif pos.x in (1, 6): return Piece(Knight(), player_id)
            elif pos.x in (2, 5): return Piece(Bishop(), player_id)
            elif pos.x == 3: return Piece(Queen(), player_id)
            elif pos.x == 4: return Piece(King(), player_id)

        elif pos.y in (1, 6): return Piece(Pawn(), 0 if pos.y == 1 else 1)

    def check(self, state):

        king = state.find_pieces(state.turn.current_id, King())[0]
        next_state = state.end_turn()
        return any(piece.type.move_valid(next_state, piece, king.pos)
            for piece in state.find_pieces(state.turn.next_id))

    #def check_mate(self, state, player):
    #    return not any(self.move_valid(state, piece, x, y)
    #        for x in range(0, self.width)
    #        for y in range(0, self.height)
    #        for piece in state.find_pieces(player_id))
