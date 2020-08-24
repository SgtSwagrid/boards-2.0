from .common.game import *


class SoldierPiece(PieceType):

    ID = 0
    TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']
    STAGE = 1

    def move_valid(self, state, piece, pos):

        if not state.turn.stage == self.STAGE or\
            not piece.pos.straight(pos): return False

        direction = piece.pos.direction(pos)
        kernel = RayKernel(state.game.SHAPE, direction)
        return pos == kernel.extent(state, piece.pos)


class NeutronPiece(SoldierPiece):

    ID = 1
    TEXTURES = ['connectfour/red_dot.png']
    STAGE = 0


class Neutron(Game):

    ID = 14
    NAME = 'Neutron'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(WIDTH := 5, HEIGHT := 5)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.m.wikipedia.org/wiki/Neutron_(game)'

    PIECES = [SoldierPiece(), NeutronPiece()]
    HANDLERS = [MoveHandler(PIECES, capture_enemy=False)]

    def on_action(self, state):

        neuron = state.find_pieces(type=NeutronPiece())[0]

        if state.turn.stage == 0:

            if neuron.pos.y in [0, self.HEIGHT - 1]:
                return state.end_game(0 if neuron.pos.y == 0 else 1)

            elif all(BoxKernel(self.SHAPE).filled(state, piece.pos)
                    for piece in state.find_pieces(state.turn.next_id)):
                return state.end_game(state.turn.next_id)

            else: return state.end_stage()

        elif state.turn.stage == 1:

            if BoxKernel(self.SHAPE).filled(state, neuron.pos):
                return state.end_game(state.turn.current_id)

            else: return state.end_turn()

    def on_setup(self, num_players):

        return super().on_setup(num_players).end_stage()

    def initial_piece(self, num_players, pos):

        if pos.y == 0: return Piece(SoldierPiece(), 0)
        elif pos.y == self.HEIGHT - 1: return Piece(SoldierPiece(), 1)
        elif pos.x == self.WIDTH // 2 and pos.y == self.HEIGHT // 2:
            return Piece(NeutronPiece(), -1)
