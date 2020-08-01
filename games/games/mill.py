from .common.game import *
from .common.handler import *

#  note to self: phase 1 through 3 are hardcoded conditionals rather than actual variables


class Mill(Game):

    name = "Mill"
    id = 4
    width = 11
    height = 11
    players = 2

    validPoint = [
        (0, 10), (0, 5), (0, 0), (2, 8), (2, 5), (2, 2), (4, 6), (4, 5), (4, 4), (5, 10), (5, 8), (5, 6), (5, 4),
        (5, 2), (5, 0), (6, 6), (6, 5), (6, 4), (8, 8), (8, 5), (8, 2), (10, 10), (10, 5), (10, 0)
    ]

    class MillPiece(PieceType):
        id = 0

        #  a piece of the active player can be placed iff not all pieces have been placed yet = before turn 18
        def place_valid(self, state, piece):
            if state.turn.ply < 18 and state.turn.stage == 0:
                if (piece.x, piece.y) in Mill.validPoint and not state.pieces[piece.x][piece.y]:
                    return True
            else:
                return False

        #  a piece owned by the active player can be moved iff all pieces have already been placed = after turn 17
        def move_valid(self, state, piece, x_to, y_to):
            if state.turn.ply >= 18 and state.turn.stage == 0:
                if (x_to, y_to) in Mill.validPoint and not state.pieces[x_to][y_to]:
                    return True
            else:
                return False

        #  after moving a piece a NEW mill might have been formed iff that is the case remove one opponents piece
        def move_piece(self, state, piece, x_to, y_to):
            state = state.move_piece(piece, x_to, y_to)
            #  I am sorry
            if y_to != piece.y:
                if y_to in [n*2 for n in range(0, 5)]:
                    foo = True
                    for x in [x for (x, y_to) in Mill.validPoint]:
                        foo = foo * state.friendly(x, y_to)
                    if foo:
                        state = state.end_stage()
                    else:
                        state = state.end_turn()
                elif y_to == 5:
                    foo = True
                    bar = True
                    for x in [x for (x, y_to) in Mill.validPoint]:
                        if x < 5:
                            foo = foo * state.friendly(x, y_to)
                        elif x > 5:
                            bar = bar * state.friendly(x, y_to)
                    if foo or bar:
                        state = state.end_stage()
                    else:
                        state = state.end_turn()
            return state

        #  a piece may only removed IFF a mill has been formed before(state.stage == 1) and it's an opponent's
        def remove_valid(self, state, piece):
            return state.turn.stage == 1 and state.enemy(piece.x, piece.y)

        def texture(self, owner):
            if owner == 0:
                return 'games/img/misc/white_dot.png'
            else:
                return 'games/img/misc/black_dot.png'

    types = [MillPiece()]

    handlers = [PlaceHandler(MillPiece()), MoveHandler(), RemoveHandler()]

    #  pieces need only be selected when to be moved and in no other case
    def moveable(self, state, piece):
        return state.turn.stage == 0 and state.friendly(piece.x, piece.y)

    #  drawing colors for (1)tiles/points where pieces can be (2)tiles/lines in between and (3)every other tile
    def background(self, x, y):
        if (x, y) in self.validPoint:
            return '#FDCB6E'
        elif x == 10 or x == 0 or y == 10 or y == 0 or (1 < x < 9 and y == 2) or (1 < x < 9 and y == 8) or \
            (1 < y < 9 and x == 2) or (1 < y < 9 and x == 8) or ((5 < x or x < 5) and y == 5) or\
                ((5 < y or y < 5) and x == 5):
            return '#55EAFF'
        else:
            return '#FFEAA7'

    # def find_mills(self, state, pieces, x, y):
    #     next_x = 0
    #     next_y = 0
    #     for possible_x in range(x, 10):
    #         if (possible_x, y) in self.validPoint:
    #             next_x = possible_x
    #     if next_x == 0:
    #         return self.mine(state, pieces, x, y)
    #     if self.mine(state, pieces, x, y) and self.find_mills(state, pieces, next_x, y):
    #         pass
    #     return False
