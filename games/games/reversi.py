from .game import Game, Piece

class Reversi(Game):

    name = "Reversi"
    id = 3

    width = 8
    height = 8

    def initial(self, x, y):
        return 0, 0

    def scale(self, x, y):
        return 1, 1

    def colour(self, x, y):
        if (x + y) % 2 == 0: return '#ffeaa7'
        else: return '#fdcb6e'
