from .tictactoe import *


class Quixo(TicTacToe):

    ID = 10
    NAME = 'Quixo'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(5, 5)
    INFO = 'https://en.wikipedia.org/wiki/Tic-tac-toe_variants#Quixo'

    TARGET = 5

    class PlayerPiece(PieceType):
        ID = 0
        TEXTURES = ['misc/naught.png', 'misc/cross.png']

    class EmptyPiece(PieceType):
        ID = 1
        COLOUR = ['#ffffff']

        def colour(self, piece, state):
            return '#ffffff'

    PIECES = [PlayerPiece(), EmptyPiece()]
    HANDLERS = [MoveHandler(hints=True)]

    def initial_piece(self, num_players, x, y):
        return Piece(self.EmptyPiece(), owner_id=-1)

    def move_valid(self, state, piece, x_to, y_to):
        width_c = state.game.SHAPE.width - 1
        height_c = state.game.SHAPE.height - 1

        return (not (piece.x == x_to and piece.y == y_to)) and\
               ((x_to == 0 and y_to == piece.y) or
                (x_to == width_c  and y_to == piece.y) or
                (x_to == piece.x and y_to == 0) or
                (x_to == piece.x and y_to == height_c))

    def moveable(self, state, piece):
        x = piece.x
        y = piece.y

        if state.game.SHAPE.in_bounds(x, y) and \
               (x == state.game.SHAPE.width - 1 or y == state.game.SHAPE.height - 1
                or x == 0 or y == 0) and \
               (state.friendly(x, y) or state.pieces[x][y].owner_id == -1):
            print("Can move", x, y)

        return state.game.SHAPE.in_bounds(x, y) and \
               (x == state.game.SHAPE.width - 1 or y == state.game.SHAPE.height - 1
                or x == 0 or y == 0) and \
               (state.friendly(x, y) or state.pieces[x][y].owner_id == -1)

    def move_piece(self, state, piece, x_to, y_to):
        dist_x = x_to - piece.x
        dist_y = y_to - piece.y
        dir_x = self.sign(dist_x)
        dir_y = self.sign(dist_y)

        print('dirs', dir_x, dir_y, dist_x, dist_y)

        state = state.remove_piece(piece)

        # shift all pieces

        for i in range(1, 10):
            x_new = piece.x + i * dir_x
            y_new = piece.y + i * dir_y

            print("Recurse ", x_new, y_new, dir_x, dir_y, " piece ") #, state.pieces[x_new][y_new])

            if state.game.SHAPE.in_bounds(x_new, y_new):
                state = state.move_piece(state.pieces[x_new][y_new], x_new - dir_x, y_new - dir_y)
            else:
                break

        # insert a piece of the player
        state = state.place_piece(Piece(self.PlayerPiece(), state.turn.current_id, x_to, y_to))

        return state

    def action(self, state, action):
        game_ended = self.has_run(state, state.action.piece)
        game_draw = not game_ended and all([isinstance(state.pieces[x][y].type, self.PlayerPiece)
            for x in range(0, self.SHAPE.width)
            for y in range(0, self.SHAPE.height)])

        return state.end_turn() if not (game_ended or game_draw)\
            else state.end_game(winner_id=state.turn.current_id if not game_draw else -1)

    def sign(self, value):
        if value < 0:
            return -1
        elif value == 0:
            return 0
        else:
            return 1