from .common.game import *
from .common.handlers import *
from .common.backgrounds import Checkerboard
from .common.shapes import Rectangle


class Reversi(Game):

    ID = 3
    NAME = 'Reversi'
    BACKGROUND = Checkerboard(['#27AE60', '#2ECC71'])
    SHAPE = Rectangle(8, 8)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.wikipedia.org/wiki/Reversi'

    class ReversiPiece(PieceType):
        ID = 0
        TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']

    PIECES = [ReversiPiece()]
    HANDLERS = [PlaceHandler(ReversiPiece())]

    MODIFIED_COLOUR = '#16a085'

    def setup(self, num_players):
        return super().setup(num_players)\
            .add_score(0, 2)\
            .add_score(1, 2)

    def initial_piece(self, num_players, x, y):
        x_mid = self.SHAPE.width // 2 - 1
        y_mid = self.SHAPE.height // 2 - 1

        # Centre arrangement 2x2
        if (x == x_mid and y == y_mid) or (x == x_mid + 1 and y == y_mid + 1):
            return Piece(self.ReversiPiece(), 0, x, y)  # White
        if (x == x_mid and y == y_mid + 1) or (x == x_mid + 1 and y == y_mid):
            return Piece(self.ReversiPiece(), 1, x, y)  # Black
        return None

    def place_valid(self, state, piece):
        return self.SHAPE.in_bounds(piece.x, piece.y) and\
                not state.pieces[piece.x][piece.y] and\
                len(self.flips(state, piece)) > 0

    def place_piece(self, state, piece):

        state = state.place_piece(piece).add_score(state.turn.current_id, 1)

        flips = self.flips(state, piece)

        for pos in flips:
            state = state\
                .add_score(state.pieces[pos[0]][pos[1]].owner_id, -1)\
                .add_score(state.turn.current_id, 1)\
                .place_piece(Piece(self.ReversiPiece(), state.turn.current_id, pos[0], pos[1]))

        return state

    def action(self, state, action):
        skipped_turns = 1
        game_ended = False

        # Loop through all players after the current player once
        for p in state.player_states:
            # Get the state by skipping X turns, 1 is next player
            state_next_turn = state.end_turn(skipped_turns)

            if not self.has_moves(state_next_turn):
                skipped_turns += 1
                if state_next_turn.turn.current_id == state.turn.current_id:
                    game_ended = True
            else:  # This player has a turn at 'skip' skips
                break

        # if skip > 1: print("Game ended" if game_ended else (str(skip-1)) + " turns skipped")
        return state.end_turn(skipped_turns) if not game_ended \
            else state.end_game()

    def flips(self, state, piece):
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, -1], [-1, 1]]
        flips = []

        for dir in directions:
            sub_flips = []

            for i in range(1, max(self.SHAPE.width, self.SHAPE.height)):
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

    def has_moves(self, state):
        '''Returns true if the current state's player has a turn they can play'''
        for x in range(self.SHAPE.width):
            for y in range(self.SHAPE.height):
                if not state.pieces[x][y]:
                    if self.place_valid(state, Piece(self.ReversiPiece(), state.turn.current_id, x, y)):
                        return True
        return False
