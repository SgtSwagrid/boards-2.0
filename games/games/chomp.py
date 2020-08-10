from .common.game import *
from .common.handlers import *
from .common.shapes import Rectangle


class Chomp(Game):

    ID = 8
    NAME = 'Chomp'
    BACKGROUND = Background('#FDCB6E')
    SHAPE = Rectangle(4, 5)
    PLAYER_NAMES = ['Red', 'Blue']

    class ChompPiece(PieceType):
        ID = 0
        COLOURS = ['#E74C3C', '#3498DB']

    PIECES = [ChompPiece()]
    HANDLERS = [PlaceHandler(ChompPiece(), hints=False)]

    def place_valid(self, state, piece):
        return state.game.SHAPE.in_bounds(piece.x, piece.y) and\
                not state.pieces[piece.x][piece.y]

    def place_piece(self, state, piece):
        player_score = state.player_states[state.turn.current_id].score
        state = state.place_piece(piece)
        state = self.capture(state, piece)
        player_score_after = state.player_states[state.turn.current_id].score

        game_finished = all([state.pieces[x][y]
            for x in range(self.SHAPE.width)
            for y in range(self.SHAPE.height)
            if (x % 2 == 1 and y % 2 == 1)])

        return state.end_game() \
            if game_finished else (state.end_turn()
                                   if player_score == player_score_after else state)