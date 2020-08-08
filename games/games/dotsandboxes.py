from .common.game import *
from .common.handler import *


class DotsAndBoxes(Game):

    ID = 7
    NAME = 'Dots and Boxes'
    SIZE = (6 * 2 + 1, 6 * 2 + 1)
    PLAYERS = (2, 2)
    PLAYER_NAMES = ['Red', 'Blue']

    BOX_SIZE = 5

    class EdgePiece(PieceType):
        ID = 0
        COLOURS = ['#E74C3C', '#3498DB']

    class CapturePiece(PieceType):
        ID = 1
        COLOURS = ['#FAB1A0', '#74B9FF']

    PIECES = [EdgePiece(), CapturePiece()]
    HANDLERS = [PlaceHandler(EdgePiece(), hints=False)]

    def background_colour(self, x, y):
        return self.gingham('#FDCB6E', '#2F3640', '#FFEAA7', x, y)

    def tile_width(self, x, y):
        return 1 if x % 2 == 0 else self.BOX_SIZE

    def tile_height(self, y):
        return 1 if y % 2 == 0 else self.BOX_SIZE

    def place_valid(self, state, piece):
        return ((piece.x % 2 == 0) ^ (piece.y % 2 == 0)) and\
               state.game.in_bounds(piece.x, piece.y) and\
                not state.pieces[piece.x][piece.y]

    def place_piece(self, state, piece):
        state = state.place_piece(piece)
        state = self.capture(state, piece)

        return state.end_turn()

    def capture(self, state, piece):
        adj = self.adjacent_tiles(state, piece)

        print("Tiles for maybe capture", adj)

        for tile in adj:
            print("Looking at", tile[0], tile[1])
            print("Tile;;", state.pieces[tile[0]][tile[1]])
            print("Edges", self.adjacent_edges(state, tile[0], tile[1]))
            if not state.pieces[tile[0]][tile[1]] and\
                    all(self.adjacent_edges(state, tile[0], tile[1])):
                print("we got one", tile[0], tile[1])
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
