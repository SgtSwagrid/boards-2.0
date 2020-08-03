from .common.game import *
from .common.handler import *


class DotsAndBoxes(Game):

    name = "Dots and Boxes"
    id = 7
    width = 6 * 2 + 1
    height = 6 * 2 + 1
    players = 2

    line_width = 0.2

    class EdgePiece(PieceType):
        id = 0

        def texture(self, owner):
            if owner == 0:
                return 'games/img/dotsandboxes/red_edge.png'  # Player 1 is Red
            else:
                return 'games/img/dotsandboxes/blue_edge.png'  # Player 2 is Blue

    class CapturePiece(PieceType):
        id = 1

        def texture(self, owner):
            if owner == 0:
                return Texture('games/img/dotsandboxes/red_edge.png', 0.5)  # Player 1 is Red
            else:
                return Texture('games/img/dotsandboxes/blue_edge.png', 0.5)  # Player 2 is Blue

    types = [EdgePiece(), CapturePiece()]
    handlers = [PlaceHandler(EdgePiece())]

    def background(self, x, y):
        if x % 2 == 0 and y % 2 == 0: return '#000000'
        if x % 2 == 0 or y % 2 == 0 == 0: return '#FDCB6E'
        else: return '#FFEAA7'

    def scale(self, x, y):
        if x % 2 == 0 and y % 2 == 0: return self.line_width, self.line_width
        if x % 2 == 0: return self.line_width, 1
        if y % 2 == 0: return 1, self.line_width
        else: return 1, 1

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
