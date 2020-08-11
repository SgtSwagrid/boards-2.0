from .common.game import *
from .common.handlers import *
from .common.shapes import Rectangle
from .tictactoe import TicTacToe


class ConnectFour(TicTacToe):

    ID = 5
    NAME = 'Connect Four'
    SHAPE = Rectangle(7, 6)
    PLAYER_NAMES = ['Yellow', 'Red']
    INFO = 'https://en.wikipedia.org/wiki/Connect_Four'

    TARGET = 4

    class ConnectFourPiece(PieceType):
        ID = 0
        TEXTURES = ['connectfour/yellow_dot.png', 'connectfour/red_dot.png']

    PIECES = [ConnectFourPiece()]
    HANDLERS = [PlaceHandler(ConnectFourPiece())]

    def place_valid(self, state, piece):
        return state.open(piece.x, piece.y) and\
            not state.open(piece.x, piece.y - 1)