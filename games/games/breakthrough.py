from .common.game import *


class BreakthroughPiece(PieceType):

    ID = 0
    TEXTURES = ['chess/white_pawn.png', 'chess/black_pawn.png']

    def move_valid(self, state, piece, pos):

        return pos.y - piece.pos.y == [1, -1][piece.owner_id] and\
            ((state.enemy(pos) and (pos.x - piece.pos.x) in [-1, 1]) or
            (state.open(pos) and (pos.x - piece.pos.x) in [-1, 0, 1]))


class Breakthrough(Game):

    ID = 13
    NAME = 'Breakthrough'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(WIDTH := 8, HEIGHT := 8)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.m.wikipedia.org/wiki/Breakthrough_(board_game)'

    PIECES = [BreakthroughPiece()]
    HANDLERS = [MoveHandler(PIECES)]

    def on_action(self, state):

        home = [self.HEIGHT - 1, 0][state.turn.current_id]
        if state.action.new_pos.y == home or\
                not any(state.find_pieces(state.turn.next_id)):

            return state.end_game(state.turn.current_id)

        else: return state.end_turn()

    def initial_piece(self, num_players, pos):

        if pos.y <= 1: return Piece(BreakthroughPiece(), 0)
        elif pos.y >= self.HEIGHT - 2: return Piece(BreakthroughPiece(), 1)
