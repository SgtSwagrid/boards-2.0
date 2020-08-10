from .common.game import *
from .common.handlers import *
from .common.shapes import Rectangle


class Clobber(Game):

    ID = 9
    NAME = 'Clobber'
    BACKGROUND = Checkerboard(['#FFFFFF', '#F0F0F0'])
    SHAPE = Rectangle(5, 6)
    PLAYER_NAMES = ['White', 'Black']

    class ClobberDot(PieceType):
        ID = 0
        TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']

    PIECES = [ClobberDot()]
    HANDLERS = [MoveHandler()]

    def piece(self, num_players, x, y):
        if (x+y) % 2 == 0:
            return Piece(self.ClobberDot(), 0, x, y)  # White
        else:
            return Piece(self.ClobberDot(), 1, x, y)  # Black

    def move_valid(self, state, piece, x_to, y_to):
        return (abs(x_to - piece.x) <= 1 ^ abs(y_to - piece.y) <= 1) and\
            state.game.SHAPE.in_bounds(x_to, y_to) and\
            state.pieces[x_to][y_to] and\
            state.pieces[x_to][y_to].owner_id != piece.owner_id

    def move_piece(self, state, piece, x_to, y_to):
       return state.move_piece(piece, x_to, y_to)

    def action(self, state, action):
        game_finished = not any(self.has_move(state, piece_e)
                                for piece_e in state.find_pieces(player_id=state.turn.next_id))

        return state.end_turn() if not game_finished else state.end_game(winner_id=state.turn.current_id)

    def has_move(self, state, piece):
        return any(self.move_valid(state, piece, piece.x + dx, piece.y + dy)
                   for dx in [-1, 0, 1]
                   for dy in [-1, 0, 1])
