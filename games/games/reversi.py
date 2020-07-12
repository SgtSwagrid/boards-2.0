from .game import Game, Piece

class Reversi(Game):

    name = "Reversi"
    id = 3

    width = 8
    height = 8

    def initial(self, x, y):
        return 0, 0

    def colour(self, x, y):
        if (x + y) % 2 == 0: return '#00ff00'
        else: return '#00aa00'
