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

    types = [ReversiPiece()]

    def place_valid(self, state, pieces, type, owner_id, x, y):
        return self.in_bounds(x, y) and \
                not pieces[x][y] and \
                len(self.flips(state, pieces, owner_id, x, y)) > 0

    def place_piece(self, state, pieces, type, owner_id, x, y):
        state.place_piece(self.ReversiPiece(), owner_id, x, y)

        flips = self.flips(state, pieces, owner_id, x, y)

        for pos in flips:
            state.place_piece(self.ReversiPiece(), owner_id, pos[0], pos[1])

        state.end_turn()

    def initial(self, x, y):

        x_mid = self.width // 2 - 1
        y_mid = self.height // 2 - 1

        # Centre arrangement 2x2
        if (x == x_mid and y == y_mid) or (x == x_mid + 1 and y == y_mid + 1): return self.ReversiPiece(), 1  # White
        if (x == x_mid and y == y_mid + 1) or (x == x_mid + 1 and y == y_mid): return self.ReversiPiece(), 2  # Black

        return None, 0

    def background(self, x, y):
        if (x + y) % 2 == 0: return '#88CA5E'   # Dark Green
        else: return '#D2FBA4'                  # Light Green

    def flips(self, state, pieces, owner_id, x, y):
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, -1], [-1, 1]]
        flips = []

        for dir in directions:
            sub_flips = []

            for i in range(1, max(self.width, self.height)):
                x_next = x + i * dir[0]
                y_next = y + i * dir[1]
                if self.enemy(state, pieces, x_next, y_next):
                    sub_flips.append([x_next, y_next])
                elif self.mine(state, pieces, x_next, y_next):
                    flips.extend(sub_flips)
                    break
                else:
                    break

        return flips

    def count_pieces(self, state, pieces, owner_id):
        pass

    def adjacents(self, state, pieces, owner_id):
        ''' Find all positions that are enemy to owner'''
        adjacents = []

        next_player = (state.turn + 1) % state.players

        for x in range(self.width):
            for y in range(self.height):
                if not self.exists(pieces, x, y):
                    adj = False

                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i != 0 and j != 0 and not adj:
                                x_k = x + i
                                y_k = y + j
                                if pieces[x_k][y_k].owner_id != next_player:
                                    adjacents.append([x, y])
                                    adj = True


        return adjacents