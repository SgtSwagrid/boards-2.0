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
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
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

        captures = set()

        for dir in directions()[:4]:
            run = {piece}

            for sign in [-1, 1]:
                for i in itertools.count(1):

                    pos = Vec(piece.pos.x + dir.x * sign * i,
                        piece.pos.y + dir.y * sign * i)

                    if state.friendly(pos, piece.owner_id):
                        run.add(state.piece_at(pos))
                    else: break

            if len(run) >= self.TARGET:
                captures.update(run)

        return captures
