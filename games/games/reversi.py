from .common.game import *
from .common.handler import *

class Reversi(Game):

    name = "Reversi"
    id = 3
    width = 8
    height = 8
    players = 2

    player_names = ['White', 'Black']

    class ReversiPiece(PieceType):
        id = 0

        def texture(self, piece, state, display):
            if piece.owner == 0:
                return Texture('games/img/misc/white_dot.png')  # Player 1 is White
            else:
                return Texture('games/img/misc/black_dot.png')  # Player 2 is Black

    types = [ReversiPiece()]

    handlers = [PlaceHandler(ReversiPiece())]

    modified_colour = '#16a085'

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

    def background_colour(self, x, y):
        return self.checkerboard('#27AE60', '#2ECC71', x, y)

    def place_valid(self, state, piece):
        return self.in_bounds(piece.x, piece.y) and\
                not state.pieces[piece.x][piece.y] and\
                len(self.flips(state, piece)) > 0

    def place_piece(self, state, piece):

        state = state.place_piece(piece).add_score(state.turn.current, 1)

        flips = self.flips(state, piece)

        for pos in flips:
            state = state\
                .add_score(state.pieces[pos[0]][pos[1]].owner, -1)\
                .add_score(state.turn.current, 1)\
                .place_piece(Piece(self.ReversiPiece(), state.turn.current, pos[0], pos[1]))

        skipped_turns = 1
        game_ended = False

        # Loop through all players after the current player once
        for p in state.players:
            # Get the state by skipping X turns, 1 is next player
            state_next_turn = state.end_turn(skipped_turns)

            if not self.has_moves(state_next_turn):
                skipped_turns += 1
                if state_next_turn.turn.current == state.turn.current:
                    game_ended = True
            else:   # This player has a turn at 'skip' skips
                break

        # if skip > 1: print("Game ended" if game_ended else (str(skip-1)) + " turns skipped")
        return state.end_turn(skipped_turns) if not game_ended\
            else state.end_game(winner=self.get_winner(state))

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

    def has_moves(self, state):
        '''Returns true if the current state's player has a turn they can play'''
        for x in range(self.width):
            for y in range(self.height):
                if not state.pieces[x][y]:
                    if self.place_valid(state, Piece(self.ReversiPiece(), state.turn.current, x, y)):
                        return True
        return False

    def get_winner(self, state):
        return state.players.index(max(state.players, key=lambda x:x.score))
