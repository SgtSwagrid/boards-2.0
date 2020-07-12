from .game import Game, Piece

class Chess(Game):

    name = "Chess"
    id = 2
    width = 8
    height = 8
    players = 2

    class Pawn(Piece):
        id = 0

        def texture(self, owner_id):
            if owner_id == 1: return 'games/img/chess/white_pawn.png'
            else: return 'games/img/chess/black_pawn.png'

        def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):

            dir = 1 if state.turn == 1 else -1
            home = y_from == (1 if state.turn == 1 else 6)

            straight = x_to == x_from and not pieces[x_to][y_to]
            normal = straight and y_to - y_from == dir
            double = straight and y_to - y_from == 2 * dir and home

            capture = abs(x_to - x_from) == 1 and pieces[x_to][y_to] and\
                      y_to - y_from == dir

            return normal or double or capture

    class Rook(Piece):
        id = 1

        def texture(self, owner_id):
            if owner_id == 1: return 'games/img/chess/white_rook.png'
            else: return 'games/img/chess/black_rook.png'

        def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):

            sx, sy = direction(x_from, y_from, x_to, y_to)
            d = distance(x_from, y_from, x_to, y_to)

            return ((sx == 0) ^ (sy == 0)) and\
                   path(x_from, y_from, sx, sy, d, pieces)

    class Knight(Piece):
        id = 2

        def texture(self, owner_id):
            if owner_id == 1: return 'games/img/chess/white_knight.png'
            else: return 'games/img/chess/black_knight.png'

        def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):

            dx, dy = delta(x_from, y_from, x_to, y_to)
            return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

    class Bishop(Piece):
        id = 3

        def texture(self, owner_id):
            if owner_id == 1: return 'games/img/chess/white_bishop.png'
            else: return 'games/img/chess/black_bishop.png'

        def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):

            dx, dy = delta(x_from, y_from, x_to, y_to)
            sx, sy = direction(x_from, y_from, x_to, y_to)
            d = distance(x_from, y_from, x_to, y_to)

            return (abs(dx) == abs(dy)) and\
                   path(x_from, y_from, sx, sy, d, pieces)

    class Queen(Piece):
        id = 4

        def texture(self, owner_id):
            if owner_id == 1: return 'games/img/chess/white_queen.png'
            else: return 'games/img/chess/black_queen.png'

        def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):

            dx, dy = delta(x_from, y_from, x_to, y_to)
            sx, sy = direction(x_from, y_from, x_to, y_to)
            d = distance(x_from, y_from, x_to, y_to)

            return (((sx == 0) ^ (sy == 0)) or (abs(dx) == abs(dy))) and\
                   path(x_from, y_from, sx, sy, d, pieces)

    class King(Piece):
        id = 5

        def texture(self, owner_id):
            if owner_id == 1: return 'games/img/chess/white_king.png'
            else: return 'games/img/chess/black_king.png'

        def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):
            return distance(x_from, y_from, x_to, y_to) == 1

    types = [Pawn(), Rook(), Knight(), Bishop(), Queen(), King()]

    def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):
        return not self.mine(state, pieces, x_to, y_to) and\
               super().move_valid(state, pieces, x_from, y_from, x_to, y_to)

    def selectable(self, state, pieces, x, y):
        return self.mine(state, pieces, x, y)

    def initial(self, x, y):

        if y == 0 or y == 7:
            player = 1 if y == 0 else 2

            if x == 0 or x == 7: return self.Rook(), player
            if x == 1 or x == 6: return self.Knight(), player
            if x == 2 or x == 5: return self.Bishop(), player
            if x == 3: return self.Queen(), player
            if x == 4: return self.King(), player

        if y == 1: return self.Pawn(), 1
        if y == 6: return self.Pawn(), 2

        return None, 0

def distance(x_from, y_from, x_to, y_to):
    return max(abs(x_to - x_from), abs(y_to - y_from))

def delta(x_from, y_from, x_to, y_to):
    return abs(x_to - x_from), abs(y_to - y_from)

def direction(x_from, y_from, x_to, y_to):
    return (-1 if x_to < x_from else 0 if x_to == x_from else 1),\
           (-1 if y_to < y_from else 0 if y_to == y_from else 1)

def path(x, y, sx, sy, d, pieces):
    return all(map(lambda r: not pieces
    [x + sx * r][y + sy * r], range(1, d)))