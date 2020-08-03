from .common.game import *
from .common.handler import *


class DotsAndBoxes(Game):

    name = "Dots and Boxes"
    id = 7
    width = 6 * 2 + 1
    height = 6* 2 + 1
    players = 2

    line_width = 0.1

    class EdgePiece(PieceType):
        id = 0

        def texture(self, owner):
            if owner == 0:
                return 'games/img/dotsandboxes/red_edge.png'  # Player 1 is Red
            else:
                return 'games/img/dotsandboxes/blue_edge.png'  # Player 2 is Blue

    types = [EdgePiece()]
    handler = [PlaceHandler(EdgePiece())]

    def background(self, x, y):
        if x % 2 == 0 and y % 2 == 0: return '#000000'
        if x % 2 == 0 or y % 2 == 0 == 0: return '#FDCB6E'
        else: return '#FFEAA7'

    def scale(self, x, y):
        if x % 2 == 0 and y % 2 == 0: return self.line_width, self.line_width
        if x % 2 == 0: return self.line_width, 1
        if y % 2 == 0: return 1, self.line_width
        else: return 1, 1