from .common.game import *
from .common.state import Piece
from .common.handlers import MoveHandler
from .common.shapes import Rectangle


class BreakthroughPiece(PieceType):

    ID = 0
    TEXTURES = ['chess/white_pawn.png', 'chess/black_pawn.png']

    def move_valid(self, state, piece, x_to, y_to):

        return y_to - piece.y == [1, -1][piece.owner_id] and\
            ((state.enemy(x_to, y_to) and (x_to - piece.x) in [-1, 1]) or
            (state.open(x_to, y_to) and (x_to - piece.x) in [-1, 0, 1]))


class Breakthrough(Game):

    ID = 13
    NAME = 'Breakthrough'
    SHAPE = Rectangle(WIDTH := 8, HEIGHT := 8)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.m.wikipedia.org/wiki/Breakthrough_(board_game)'

    PIECES = [BreakthroughPiece()]
    HANDLERS = [MoveHandler(PIECES)]

    def on_action(self, state):

        if state.action.y_to == [self.HEIGHT - 1, 0][state.turn.current_id] or\
                not any(state.find_pieces(state.turn.next_id)):

            return state.end_game(state.turn.current_id)

        else: return state.end_turn()

    def initial_piece(self, num_players, x, y):

        if y <= 1: return Piece(BreakthroughPiece(), 0)
        elif y >= self.HEIGHT - 2: return Piece(BreakthroughPiece(), 1)
