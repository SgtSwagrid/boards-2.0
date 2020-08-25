from .common.game import *


class Amazon(PieceType):

    ID = 0
    TEXTURES = ['chess/white_queen.png', 'chess/black_queen.png']

    def move_valid(self, state, piece, pos):

        return state.turn.stage == 0 and \
               not state.piece(pos) and \
               is_queen_move(state, piece.pos, pos)


class Arrow(PieceType):

    ID = 1
    TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']

    def place_valid(self, state, piece):

        if state.turn.stage == 0: return False

        return state.turn.stage == 1 and\
            not state.pieces[piece.x][piece.y] and\
            is_queen_move(state, piece.pos, piece.x, piece.y)


class Amazons(Game):

    ID = 6
    NAME = 'Amazons'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(10, 10)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.wikipedia.org/wiki/Game_of_the_Amazons'

    PIECES = [Amazon(), Arrow()]
    HANDLERS = [MoveHandler([Amazon()]), PlaceHandler(Arrow())]

    def on_action(self, state):

        if isinstance(state.action, MoveAction):
            return state.end_stage()

        elif not all(BoxKernel(self.SHAPE).filled(state, piece.pos)
                for piece in state.find_pieces(state.turn.next_id, Amazon())):
            return state.end_turn()

        else: return state.end_game(state.turn.current_id)

    def initial_piece(self, num_players, pos):

        # Top and bottom arrangement
        tw = self.SHAPE.width // 3
        th = self.SHAPE.height // 3

        op_tw = self.SHAPE.width - 1 - tw
        op_th = self.SHAPE.height - 1 - th

        white_queens = [
            Vec(tw, 0),
            Vec(op_tw, 0),
            Vec(0, th),
            Vec(self.SHAPE.width-1, th)
        ]

        black_queens = [
            Vec(tw, self.SHAPE.height-1),
            Vec(op_tw, self.SHAPE.height-1),
            Vec(0, op_th),
            Vec(self.SHAPE.width-1, op_th)
        ]

        if pos in white_queens:
            return Piece(Amazon(), 0, pos)  # White

        if pos in black_queens:
            return Piece(Amazon(), 1, pos)  # Black


def is_queen_move(state, pos_from, pos_to):

    dpos = delta(pos_from, pos_to)
    spos = direction(pos_from, pos_to)
    d = distance(pos_from, pos_to)
    return (((spos.x == 0) ^ (spos.y == 0)) or (abs(dpos.x) == abs(dpos.y))) and\
        path(pos_from, spos, d, state.pieces)

def distance(pos_from, pos_to):
    return max(abs(pos_to.x - pos_from.x), abs(pos_to.y - pos_from.y))

def delta(pos_from, pos_to):
    return Vec(abs(pos_to.x - pos_from.x), abs(pos_to.y - pos_from.y))

def direction(pos_from, pos_to):
    return (-1 if pos_to.x < pos_from.x else 0 if pos_to.x == pos_from.x else 1),\
            (-1 if pos_to.y < pos_from.y else 0 if pos_to.y == pos_from.y else 1)

def path(pos, spos, d, pieces):
    return all(map(lambda r: not pieces
    [pos.x + spos.x * r][pos.y + spos.y * r], range(1, d)))
