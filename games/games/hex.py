from .common.game import *


BOTTOM = LEFT = 0x01
TOP = RIGHT = 0x10


class HexPiece(PieceType):

    ID = 0
    COLOURS = ['#EB4D4B', '#4A69BD']

    def place_piece(self, state, piece):

        state = state.place_piece(piece)

        sides = self.side(state, piece)
        for n in self.neighbours(state, piece):
            sides |= n.mode

        return self.link(state, piece, sides)

    def link(self, state, piece, sides):

        state = state.set_piece_mode(piece, piece.mode | sides)

        for n in self.neighbours(state, piece):
            if (n.mode ^ sides) & sides:
                state = self.link(state, n, sides)

        return state

    def neighbours(self, state, piece):

        kernel = HexKernel(state.game.SHAPE)
        return kernel.find_pieces(state, piece.pos, piece.owner_id)

    def side(self, state, piece):

        if piece.owner_id == 0:
            if piece.pos.y == 0: return BOTTOM
            elif piece.pos.y == state.game.HEIGHT - 1: return TOP

        elif piece.owner_id == 1:
            if piece.pos.x == 0: return LEFT
            elif piece.pos.x == state.game.WIDTH - 1: return RIGHT

        return 0


class HexBackground(HexCheckerboard):

    def __init__(self):
        super().__init__(['#FFFFFF', '#F1F2F6', '#DFE4EA'])

    def colour(self, pos):

        if pos.y in [0, Hex.HEIGHT - 1] and\
                pos.x not in [0, Hex.WIDTH - 1]:
            return '#EA8685'

        elif pos.x in [0, Hex.WIDTH - 1] and\
                pos.y not in [0, Hex.HEIGHT - 1]:
            return '#778BEB'

        elif pos.x in [0, Hex.WIDTH - 1] and\
                pos.y in [0, Hex.HEIGHT - 1]:
            return '#786FA6'

        else: return super().colour(pos)


class Hex(Game):

    ID = 17
    NAME = 'Hex'
    BACKGROUND = HexBackground()
    SHAPE = SlantedHex(WIDTH := 11, HEIGHT := 11)
    PLAYER_NAMES = ['Red', 'Blue']
    INFO = 'https://en.wikipedia.org/wiki/Hex_%28board_game%29'

    PIECES = [HexPiece()]
    HANDLERS = [PlaceHandler(HexPiece(), hints=False)]

    def on_action(self, state):

        mode = state.action.piece.mode

        if (mode & BOTTOM and mode & TOP) or (mode & LEFT and mode & RIGHT):
            return state.end_game(state.turn.current_id)
        else: return state.end_turn()
