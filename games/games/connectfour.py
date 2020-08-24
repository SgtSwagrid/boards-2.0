from .tictactoe import *


class ConnectFourPiece(TicTacToePiece):

    ID = 0
    TEXTURES = ['connectfour/yellow_dot.png', 'connectfour/red_dot.png']

    def place_valid(self, state, piece):
        return not state.open(piece.x, piece.y - 1)


class ConnectFour(TicTacToe):

    ID = 5
    NAME = 'Connect Four'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(7, 6)
    PLAYER_NAMES = ['Yellow', 'Red']
    INFO = 'https://en.wikipedia.org/wiki/Connect_Four'

    PIECES = [ConnectFourPiece()]
    HANDLERS = [PlaceHandler(ConnectFourPiece())]

    TARGET = 4
