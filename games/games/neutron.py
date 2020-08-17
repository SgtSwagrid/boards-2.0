from .common.game import *
from .common.handlers import MoveHandler
from .common.shapes import Rectangle
from .common.util import *


class SoldierPiece(PieceType):

    ID = 0
    TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']
    STAGE = 1

    def move_valid(self, state, piece, x_to, y_to):

        if not state.turn.stage == self.STAGE or\
            not is_straight(piece.x, piece.y, x_to, y_to): return False

        dx, dy = direction(piece.x, piece.y, x_to, y_to)
        return (x_to, y_to) == state.raycast(piece.x, piece.y, dx, dy)


class NeutronPiece(SoldierPiece):

    ID = 1
    TEXTURES = ['connectfour/red_dot.png']
    STAGE = 0


class Neutron(Game):

    ID = 14
    NAME = 'Neutron'
    SHAPE = Rectangle(WIDTH := 5, HEIGHT := 5)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.m.wikipedia.org/wiki/Neutron_(game)'

    PIECES = [SoldierPiece(), NeutronPiece()]
    HANDLERS = [MoveHandler(PIECES, capture_enemy=False)]

    def on_action(self, state):

        neuron = state.find_pieces(type=NeutronPiece())[0]

        if state.turn.stage == 0:

            if neuron.y in [0, self.HEIGHT - 1]:
                return state.end_game(0 if neuron.y == 0 else 1)

            elif state.all_surrounded(state.turn.current_id):
                return state.end_game(state.turn.next_id)

            else: return state.end_stage()

        elif state.turn.stage == 1:

            if state.surrounded(neuron):
                return state.end_game(state.turn.current_id)

            else: return state.end_turn()

    def on_setup(self, num_players):

        return super().on_setup(num_players).end_stage()

    def initial_piece(self, num_players, x, y):

        if y == 0: return Piece(SoldierPiece(), 0)
        elif y == self.HEIGHT - 1: return Piece(SoldierPiece(), 1)
        elif x == self.WIDTH // 2 and y == self.HEIGHT // 2:
            return Piece(NeutronPiece(), -1)
