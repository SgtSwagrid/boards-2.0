from .common.game import *
from .common.handlers import *
from .common.shapes import Rectangle


class ChompBoard(Checkerboard):

    def texture(self, x, y):
        if x == 0 and y == 0:
            return ['misc/poison.png']
        else:
            return super().texture(x, y)


class Chomp(Game):

    ID = 8
    NAME = 'Chomp'
    BACKGROUND = ChompBoard(['#5D4037', '#8D6E63'])
    SHAPE = Rectangle(6, 5)
    PLAYER_NAMES = ['Purple', 'Yellow']
    INFO = 'https://en.wikipedia.org/wiki/Chomp'

    class ChompPiece(PieceType):
        ID = 0
        COLOURS = ['#8c7ae6', '#9c88ff', '#e1b12c', '#fbc531']

        def colour(self, piece, state):
            return self.COLOURS[2*piece.owner_id] if (piece.x + piece.y) % 2 == 0 else self.COLOURS[piece.owner_id*2+1]

    PIECES = [ChompPiece()]
    HANDLERS = [PlaceHandler(ChompPiece(), hints=False)]

    def place_valid(self, state, piece):
        return state.game.SHAPE.in_bounds(piece.x, piece.y) and\
                not state.pieces[piece.x][piece.y]

    def action(self, state, action):
        l_piece = state.action.piece
        # Eaten the poison
        game_finished = (l_piece.x == 0 and l_piece.y == 0)

        return state.end_turn() if not game_finished \
            else state.end_game(winner_id=state.turn.next_id)

    def place_piece(self, state, piece):
        state = state.place_piece(piece)

        fill_piece = Piece(self.ChompPiece(), owner_id=piece.owner_id, x=piece.x, y=piece.y)

        for x in range(piece.x, state.game.SHAPE.width):
            for y in range(piece.y, state.game.SHAPE.height):
                if not state.pieces[x][y]:
                    state = state.place_piece(fill_piece.at(x, y))

        return state
