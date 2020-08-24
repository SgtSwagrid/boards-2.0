from .common.game import *
import itertools


class TicTacToePiece(PieceType):

    ID = 0
    TEXTURES = ['misc/naught.png', 'misc/cross.png']

    def colour(self, piece, state):
        return [None, state.game.RUN_COLOUR][piece.mode]


class TicTacToe(Game):

    ID = 1
    NAME = 'Tic Tac Toe'
    SHAPE = Rectangle(3, 3)
    PLAYER_NAMES = ['Naughts', 'Crosses']
    INFO = 'https://en.wikipedia.org/wiki/Tic-tac-toe'

    PIECES = [TicTacToePiece()]
    HANDLERS = [PlaceHandler(TicTacToePiece())]

    TARGET = 3
    RUN_COLOUR = '#16A085'

    def on_action(self, state):

        if any(pieces := self.captures(state, state.action.piece)):

            for piece in pieces:
                state = state.set_piece_mode(piece, 1)

            return state.end_game(state.turn.current_id)

        elif state.turn.ply + 1 == self.SHAPE.width * self.SHAPE.height:
            return state.end_game()

        else: return state.end_turn()

    def captures(self, state, piece):

        directions = [[1, 0], [0, 1], [1, 1], [1, -1]]
        captures = set()

        for dir in directions:
            run = {piece}

            for sign in [-1, 1]:
                for i in itertools.count(1):

                    x = piece.x + dir[0] * sign * i
                    y = piece.y + dir[1] * sign * i

                    if state.friendly(x, y, piece.owner_id):
                        run.add(state.pieces[x][y])
                    else: break

            if len(run) >= self.TARGET:
                captures.update(run)

        return captures
