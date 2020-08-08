from .common.game import *
from .common.handler import *
from .tictactoe import TicTacToe


class ConnectFour(TicTacToe):

    ID = 5
    NAME = 'Connect Four'
    SIZE = (7, 6)
    PLAYERS = (2, 2)
    PLAYER_NAMES = ['Yellow', 'Red']

    TARGET = 4

    class ConnectFourPiece(PieceType):
        ID = 0
        TEXTURES = ['connectfour/yellow_dot.png', 'connectfour/red_dot.png']

    PIECES = [ConnectFourPiece()]
    HANDLERS = [PlaceHandler(ConnectFourPiece())]

    def place_valid(self, state, piece):
        return self.in_bounds(piece.x, piece.y) and\
                not state.pieces[piece.x][piece.y] and\
                self.on_floor(state, piece)

    def on_floor(self, state, piece):
        return piece.y == 0 or state.pieces[piece.x][piece.y-1]