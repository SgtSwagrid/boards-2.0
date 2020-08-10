from .common.game import *
from .common.handlers import *
from .common.backgrounds import Gingham
from .common.shapes import Table


class DotsAndBoxes(Game):

    ID = 7
    NAME = 'Dots and Boxes'
    BACKGROUND = Gingham(['#FDCB6E', '#2F3640', '#FFEAA7'])
    SHAPE = Table(6, 6, cell_width=5, cell_height=5)
    PLAYER_NAMES = ['Red', 'Blue']

    class EdgePiece(PieceType):
        ID = 0
        COLOURS = ['#E74C3C', '#3498DB']

    class CapturePiece(PieceType):
        ID = 1
        COLOURS = ['#FAB1A0', '#74B9FF']

    PIECES = [EdgePiece(), CapturePiece()]
    HANDLERS = [PlaceHandler(EdgePiece(), hints=False)]

    def place_valid(self, state, piece):
        return ((piece.x % 2 == 0) ^ (piece.y % 2 == 0)) and\
               state.game.SHAPE.in_bounds(piece.x, piece.y) and\
                not state.pieces[piece.x][piece.y]

    def place_piece(self, state, piece):
        player_score = state.player_states[state.turn.current_id].score
        state = state.place_piece(piece)
        state = self.capture(state, piece)
        player_score_after = state.player_states[state.turn.current_id].score

        return state.end_turn() if player_score == player_score_after else state

    def action(self, state, action):
        game_finished = all([state.pieces[x][y]
            for x in range(self.SHAPE.width)
            for y in range(self.SHAPE.height)
            if (x % 2 == 1 and y % 2 == 1)])

        return state if not game_finished else state.end_game()


    def capture(self, state, piece):
        adj = self.adjacent_tiles(state, piece)

        for tile in adj:
            if not state.pieces[tile[0]][tile[1]] and\
                    all(self.adjacent_edges(state, tile[0], tile[1])):
                cap_piece = Piece(self.CapturePiece(), state.turn.current_id, tile[0], tile[1])
                state = state\
                    .place_piece(cap_piece)\
                    .add_score(state.turn.current_id, 1)

        return state

    def adjacent_tiles(self, state, piece):
        return [(piece.x+dx, piece.y+dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if ((piece.x+dx) % 2 == 1 and ((piece.y+dy) % 2 == 1))
                and not (dx == 0 and dy == 0)
                and state.open(piece.x+dx, piece.y+dy)]

    def adjacent_edges(self, state, x, y):
        return [state.pieces[x+dx][y+dy]
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (((x+dx) % 2 == 0) ^ ((y+dy) % 2 == 0))
                and not (dx == 0 and dy == 0)]