from .tictactoe import TicTacToe, TicTacToePiece
from .common.handlers import PlaceHandler
from .common.shapes import Rectangle


class ConnectFourPiece(TicTacToePiece):

    ID = 0
    TEXTURES = ['connectfour/yellow_dot.png', 'connectfour/red_dot.png']

    def place_valid(self, state, piece):
        return not state.open(piece.x, piece.y - 1)


class ConnectFour(TicTacToe):

    ID = 5
    NAME = 'Connect Four'
    SHAPE = Rectangle(7, 6)
    PLAYER_NAMES = ['Yellow', 'Red']
    INFO = 'https://en.wikipedia.org/wiki/Connect_Four'

    PIECES = [ConnectFourPiece()]
    HANDLERS = [PlaceHandler(ConnectFourPiece())]

    TARGET = 4
