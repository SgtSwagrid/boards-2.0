from .game import Game, Piece


class Mill(Game):

    name = "Mill"
    id = 4
    width = 7
    height = 7
    players = 2

    validPoint = [
        (0, 6), (0, 3), (0, 0), (1, 5), (1, 3), (1, 1), (2, 4), (2, 3), (2, 2), (3, 6), (3, 5), (3, 4), (3, 2), (3, 1),
        (3, 0), (4, 4), (4, 3), (4, 2), (5, 5), (5, 3), (5, 1), (6, 6), (6, 3), (6, 0)
    ]

    class MillPiece(Piece):
        id = 0

        def texture(self, owner_id):
            if owner_id == 1:
                return 'games/img/chess/white.png'
            else:
                return 'games/img/chess/black.png'

        def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):
            pass

    types = [MillPiece()]

    def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):
        return not self.mine(state, pieces, x_to, y_to) and\
               super().move_valid(state, pieces, x_from, y_from, x_to, y_to)

    def selectable(self, state, pieces, x, y):
        return self.mine(state, pieces, x, y)

    def background(self, x, y):
        if (x, y) in super().validPoint:
            return '#FDCB6E'
        else:
            return '#FFEAA7'
