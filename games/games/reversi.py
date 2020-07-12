from .game import Game, Piece

class Reversi(Game):

    name = "Reversi"
    id = 3
    width = 8
    height = 8
    players = 2

    class Piece(state):
        id = 0

        def texture(self, owner_id):
            if owner_id == 1: return 'games/img/misc/white_dot.png'     # Player 1 is White
            else: return 'games/img/misc/black_dot.png'                 # Player 2 is Black

        '''def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):

            dir = 1 if state.turn == 1 else -1
            home = y_from == (1 if state.turn == 1 else 6)

            straight = x_to == x_from and not pieces[x_to][y_to]
            normal = straight and y_to - y_from == dir
            double = straight and y_to - y_from == 2 * dir and home

            capture = abs(x_to - x_from) == 1 and pieces[x_to][y_to] and\
                      y_to - y_from == dir

            return normal or double or capture'''

        def move_piece(self, state, pieces, x_from, y_from, x_to, y_to):
            state.move_piece(x_from, y_from, x_to, y_to)
            state.end_turn()

    types = [Piece()]

    def selectable(self, state, pieces, x, y):
        return self.mine(state, pieces, x, y)

    def initial(self, x, y):
        midX = width // 2
        midY = height // 2

        if (x == midX and y == midY) or (x == midX + 1 and y == midY + 1): return self.Piece(), 1
        if (x == midX and y == midY + 1) or (x == midX + 1 and y == midY): return self.Piece(), 2

        return None, 0

    def colour(self, x, y):
        if (x + y) % 2 == 0: return '#056608'   # Dark Green
        else: return '#08b40e'                  # Light Green
