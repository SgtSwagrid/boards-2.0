from .common.game import *


class ReversiPiece(PieceType):

    ID = 0
    TEXTURES = ['misc/white_dot.png', 'misc/black_dot.png']

    def place_valid(self, state, piece):

        return len(state.game.flips(state, piece)) > 0

    def place_piece(self, state, piece):

        state = state.place_piece(piece).add_score(state.turn.current_id, 1)
        flips = state.game.flips(state, piece)

        for pos in flips:
            state = state\
                .add_score(state.piece_at(pos).owner_id, -1)\
                .add_score(state.turn.current_id, 1)\
                .place_piece(Piece(ReversiPiece(),
                    state.turn.current_id, pos))

        return state


class Reversi(Game):

    ID = 3
    NAME = 'Reversi'
    BACKGROUND = Checkerboard(['#27AE60', '#2ECC71'])
    SHAPE = Rectangle(WIDTH := 8, HEIGHT := 8)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.wikipedia.org/wiki/Reversi'

    PIECES = [ReversiPiece()]
    HANDLERS = [PlaceHandler(ReversiPiece())]

    MODIFIED_COLOUR = '#16a085'

    def initial_piece(self, num_players, pos):

        mid = Vec(self.WIDTH // 2 - 1, self.HEIGHT // 2 - 1)

        # Centre arrangement 2x2
        if pos == mid or pos == mid + (1, 1):
            return Piece(ReversiPiece(), 0)  # White
        if pos == mid + (0, 1) or pos == mid + (1, 0):
            return Piece(ReversiPiece(), 1)  # Black

    def initial_score(self, num_players, player_id):
        return 2

    def on_action(self, state):

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

        flips = []

        for dir in directions():
            sub_flips = []

            for i in range(1, max(self.WIDTH, self.HEIGHT)):

                next = Vec(piece.pos.x + i * dir.x, piece.pos.y + i * dir.y)

                if state.enemy(next):
                    sub_flips.append(next)

                elif state.friendly(next):
                    flips.extend(sub_flips)
                    break

                else: break
        return flips

    def has_moves(self, state):

        '''Returns true if the current state's player has a turn they can play'''
        for pos in self.SHAPE.positions():
            if not state.piece_at(pos):
                if ReversiPiece().place_valid(state,
                        Piece(ReversiPiece(), state.turn.current_id, pos)):
                    return True
        return False
