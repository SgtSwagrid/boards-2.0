from .game import Game, Piece

class Reversi(Game):

    name = "Reversi"
    id = 3
    width = 8
    height = 8
    players = 2

    class ReversiPiece(Piece):
        id = 0

        def texture(self, owner_id):
            if owner_id == 1: return 'games/img/misc/white_dot.png'     # Player 1 is White
            else: return 'games/img/misc/black_dot.png'                 # Player 2 is Black

        def place_valid(self, state, pieces, owner_id, x, y):
            return not pieces[x][y]

        def place_piece(self, state, pieces, type, owner_id, x, y):
            state.place_piece(self, owner_id, x, y)
            state.end_turn()

    types = [ReversiPiece()]

    def initial(self, x, y):
        midX = self.width // 2 - 1
        midY = self.height // 2 - 1

        if (x == midX and y == midY) or (x == midX + 1 and y == midY + 1): return self.ReversiPiece(), 1
        if (x == midX and y == midY + 1) or (x == midX + 1 and y == midY): return self.ReversiPiece(), 2

        return None, 0

    def colour(self, x, y):
        if (x + y) % 2 == 0: return '#056608'   # Dark Green
        else: return '#08b40e'                  # Light Green
