from .game import Game, Piece

class TicTacToe(Game):

    name = "Tic Tac Toe"
    id = 1

    width = 3
    height = 3

    def initial(self, x, y):
        return 0, 0

    def scale(self, x, y):
        return 1, 1

    def colour(self, x, y):
        if (x + y) % 2 == 0: return '#ffeaa7'
        else: return '#fdcb6e'
