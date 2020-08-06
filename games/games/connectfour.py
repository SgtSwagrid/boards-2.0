from .common.game import *
from .common.handler import *
from .tictactoe import TicTacToe


class ConnectFour(TicTacToe):

    name = "Connect Four"
    id = 5
    width = 7
    height = 6
    players = 2
    target = 4

    player_names = ['Yellow', 'Red']

    class ConnectFourPiece(PieceType):
        id = 0

        def texture(self, piece, state, display):
            if piece.owner_id == 0:
                return Texture('games/img/connectfour/yellow_dot.png')  # Player 1 is White
            else:
                return Texture('games/img/connectfour/red_dot.png')  # Player 2 is Black

    types = [ConnectFourPiece()]
    handlers = [PlaceHandler(ConnectFourPiece())]

    def place_valid(self, state, piece):
        return self.in_bounds(piece.x, piece.y) and\
                not state.pieces[piece.x][piece.y] and\
                self.on_floor(state, piece)

    def on_floor(self, state, piece):
        if piece.y == 0:
            return True
        else:
            return state.pieces[piece.x][piece.y-1]