from .common.game import *
from .common.handler import *

class Reversi(Game):

    name = "Reversi"
    id = 3
    width = 8
    height = 8
    players = 2

    class ReversiPiece(PieceType):
        id = 0

        def texture(self, owner):
            if owner == 0: return 'games/img/misc/white_dot.png'     # Player 1 is White
            else: return 'games/img/misc/black_dot.png'                 # Player 2 is Black

    types = [ReversiPiece()]

    handlers = [PlaceHandler(ReversiPiece())]

    modified_colour = '#16a085'

    def place_valid(self, state, piece):
        return self.in_bounds(piece.x, piece.y) and\
                not state.pieces[piece.x][piece.y] and\
                len(self.flips(state, piece)) > 0

    def place_piece(self, state, piece):

        state = state.place_piece(piece)\
            .add_score(state.turn.current, 1)

        flips = self.flips(state, piece)

        for pos in flips:
            state = state\
                .add_score(state.pieces[pos[0]][pos[1]].owner, -1)\
                .add_score(state.turn.current, 1)\
                .place_piece(Piece(self.ReversiPiece(),
                    state.turn.current, pos[0], pos[1]))

        self.legal_next(state)
        return state.end_turn()

    def setup(self):
        return super().setup()\
            .add_score(0, 2)\
            .add_score(1, 2)

    def piece(self, x, y):

        x_mid = self.width // 2 - 1
        y_mid = self.height // 2 - 1

        # Centre arrangement 2x2
        if (x == x_mid and y == y_mid) or (x == x_mid + 1 and y == y_mid + 1):
            return Piece(self.ReversiPiece(), 0, x, y)  # White
        if (x == x_mid and y == y_mid + 1) or (x == x_mid + 1 and y == y_mid):
            return Piece(self.ReversiPiece(), 1, x, y)  # Black

        return None

    def background(self, x, y):
        if (x + y) % 2 == 0: return '#27ae60'   # Dark Green
        else: return '#2ecc71'                  # Light Green

    def flips(self, state, piece):
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, -1], [-1, 1]]
        flips = []

        for dir in directions:
            sub_flips = []

            for i in range(1, max(self.width, self.height)):
                x_next = piece.x + i * dir[0]
                y_next = piece.y + i * dir[1]
                if state.enemy(x_next, y_next):
                    sub_flips.append([x_next, y_next])
                elif state.friendly(x_next, y_next):
                    flips.extend(sub_flips)
                    break
                else:
                    break

        return flips

    def count_pieces(self, state, owner_id):
        pass

    def adjacents(self, state):
        ''' Find all positions that are enemy to owner'''
        adjacents = []

        next_player = (state.turn.current + 1) % self.players

        for x in range(self.width):
            for y in range(self.height):
                if not state.exists(x, y):
                    adj = False

                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            x_k = x + i
                            y_k = y + j
                            if i != 0 and j != 0 and state.exists(x_k, y_k) and not adj:
                                if state.pieces[x_k][y_k].owner != next_player:
                                    adjacents.append([x, y])
                                    adj = True

        return adjacents
