from .common.game import *
from .common.handler import *


class DotsAndBoxes(Game):

    name = "Dots and Boxes"
    id = 7
    width = 6 * 2 + 1
    height = 6 * 2 + 1
    players = 2

    player_names = ['Red', 'Blue']

    box_size = 5

    class EdgePiece(PieceType):
        id = 0

        def texture(self, piece, state, display):
            if piece.owner == 0:
                return Texture('games/img/dotsandboxes/red_edge.png')  # Player 1 is Red
            else:
                return Texture('games/img/dotsandboxes/blue_edge.png')  # Player 2 is Blue

    class CapturePiece(PieceType):
        id = 1

        def texture(self, piece, state, display):
            if piece.owner == 0:
                return Texture('games/img/dotsandboxes/red_edge.png', 0.5)  # Player 1 is Red
            else:
                return Texture('games/img/dotsandboxes/blue_edge.png', 0.5)  # Player 2 is Blue

    types = [EdgePiece(), CapturePiece()]
    handlers = [PlaceHandler(EdgePiece())]

    def background_colour(self, x, y):
        return self.gingham('#FDCB6E', '#000000', '#FFEAA7', x, y)

    def h_scale(self, x):
        return 1 if x % 2 == 0 else self.box_size

    def v_scale(self, y):
        return 1 if y % 2 == 0 else self.box_size

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
                cap_piece = Piece(self.types[1], state.turn.current, tile[0], tile[1])
                state = state\
                    .place_piece(cap_piece)\
                    .add_score(state.turn.current, 1)

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
