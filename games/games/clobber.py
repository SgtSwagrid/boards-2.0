from .common.game import *


class ClobberPiece(PieceType):

    ID = 0
    TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']

    def move_valid(self, state, piece, pos):

        return piece.pos.orth_adjacent(pos) and\
            state.enemy(pos)


class Clobber(Game):

    ID = 9
    NAME = 'Clobber'
    BACKGROUND = Checkerboard(['#FFFFFF', '#F0F0F0'])
    SHAPE = Rectangle(5, 6)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.wikipedia.org/wiki/Clobber'

    PIECES = [ClobberPiece()]
    HANDLERS = [MoveHandler(PIECES)]

    def initial_piece(self, num_players, pos):

        return Piece(ClobberPiece(), (pos.y + pos.y) % 2)

    def on_action(self, state):

        won = not any(DiamondKernel(self.SHAPE).find_pieces(
            state, piece.pos.x, piece.pos.y, state.turn.current_id)
            for piece in state.find_pieces(state.turn.next_id))

        if not won: return state.end_turn()
        else: return state.end_game(state.turn.current_id)
