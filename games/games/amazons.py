from .common.game import *


class Amazons(Game):

    ID = 6
    NAME = 'Amazons'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(10, 10)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.wikipedia.org/wiki/Game_of_the_Amazons'

    class AmazonPiece(PieceType):

        ID = 0
        TEXTURES = ['chess/white_queen.png', 'chess/black_queen.png']

        def move_valid(self, state, piece, x_to, y_to):
            return state.turn.stage == 0 and \
                not state.pieces[x_to][y_to] and \
                state.game.is_queen_move(state, piece.x, piece.y, x_to, y_to)

        def move_piece(self, state, piece, x_to, y_to):
            return state \
                .move_piece(piece, x_to, y_to)

    class ArrowPiece(PieceType):

        ID = 1
        TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']

        def place_valid(self, state, piece):
            if state.turn.stage == 0: return False
            x_from = state.action.x_to
            y_from = state.action.y_to

            return state.turn.stage == 1 and \
                not state.pieces[piece.x][piece.y] and \
                state.game.is_queen_move(state, x_from, y_from, piece.x, piece.y)

        def place_piece(self, state, piece):
            return state.place_piece(piece)

        def moveable(self, state, piece):
            return False

    PIECES = [AmazonPiece(), ArrowPiece()]
    HANDLERS = [MoveHandler(), PlaceHandler(ArrowPiece())]

    def action(self, state, action):
        if isinstance(state.action, MoveAction):
            return state.end_stage()
        else:
            state_next_turn = state.end_turn()
            return state_next_turn if state.game.can_move(state_next_turn) \
                else state_next_turn.end_game(winner_id=state.turn.current_id)

    def initial_piece(self, num_players, x, y):
        # Top and bottom arrangement
        tw = self.SHAPE.width // 3
        th = self.SHAPE.height // 3

        op_tw = self.SHAPE.width - 1 - tw
        op_th = self.SHAPE.height - 1 - th

        white_queens = [
            [tw, 0],
            [op_tw, 0],
            [0, th],
            [self.SHAPE.width-1, th]
        ]

        black_queens = [
            [tw, self.SHAPE.height-1],
            [op_tw, self.SHAPE.height-1],
            [0, op_th],
            [self.SHAPE.width-1, op_th]
        ]

        if [x, y] in white_queens:
            return Piece(self.AmazonPiece(), 0, x, y)  # White

        if [x, y] in black_queens:
            return Piece(self.AmazonPiece(), 1, x, y)  # Black

        return None

    def can_move(self, state):
        return any([state.open(piece.x + dx, piece.y + dy)
                    for dx in range(-1, 2)
                    for dy in range(-1, 2)
                    for piece in state.find_pieces(state.turn.current_id)
                    if isinstance(piece.type, self.AmazonPiece)])

    def is_queen_move(self, state, x_from, y_from, x_to, y_to):
        dx, dy = delta(x_from, y_from, x_to, y_to)
        sx, sy = direction(x_from, y_from, x_to, y_to)
        d = distance(x_from, y_from, x_to, y_to)
        return (((sx == 0) ^ (sy == 0)) or (abs(dx) == abs(dy))) and \
               path(x_from, y_from, sx, sy, d, state.pieces)

def distance(x_from, y_from, x_to, y_to):
    return max(abs(x_to - x_from), abs(y_to - y_from))


def delta(x_from, y_from, x_to, y_to):
    return abs(x_to - x_from), abs(y_to - y_from)


def direction(x_from, y_from, x_to, y_to):
    return (-1 if x_to < x_from else 0 if x_to == x_from else 1), \
            (-1 if y_to < y_from else 0 if y_to == y_from else 1)

def path(x, y, sx, sy, d, pieces):
    return all(map(lambda r: not pieces
    [x + sx * r][y + sy * r], range(1, d)))
