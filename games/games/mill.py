from .game import Game, Piece

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

    class MillPiece(Piece):
        id = 0

        #  a piece of the active player can be placed iff not all pieces have been placed yet = before turn 18
        def place_valid(self, state, pieces, owner_id, x, y):
            if state.ply < 18 and state.stage == 0:
                if (x, y) in Mill.validPoint and not pieces[x][y]:
                    return True
            else:
                return False

        #  a piece owned by the active player can be moved iff all pieces have already been placed = after turn 17
        def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):
            if state.ply >= 18 and state.stage == 0:
                if (x_to, y_to) in Mill.validPoint and not pieces[x_to][y_to]:
                    return True
            else:
                return False

        #  after moving a piece a NEW mill might have been formed iff that is the case remove one opponents piece
        def move_piece(self, state, pieces, x_from, y_from, x_to, y_to):
            state.move_piece(x_from, y_from, x_to, y_to)
            #  TODO add end_stage after if conditions for when a mill was formed
            state.end_turn()

        #  a piece may only removed IFF a mill has been formed before(state.stage == 1) and it's an opponent's
        def remove_valid(self, state, pieces, x, y):
            return state.stage == 1 and Game.enemy(state, pieces, x, y)
            #  credit to Alec / Sgt. Swagrid for optimization

        def texture(self, owner_id):
            if owner_id == 1:
                return 'games/img/chess/white.png'
            else:
                return 'games/img/chess/black.png'

    types = [MillPiece()]

    #  pieces need only be selected when to be moved and in no other case
    def selectable(self, state, pieces, x, y):
        if state.stage == 0:
            return self.mine(state, pieces, x, y)

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
