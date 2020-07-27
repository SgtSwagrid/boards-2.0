from games.games.common.state import *

class Game:

    types = []
    actions = []

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def place_valid(self, state, piece):

        return piece and self.in_bounds(piece.x, piece.y) and\
            piece.owner == state.turn.current and\
            not state.pieces[piece.x][piece.y] and\
            type.place_valid(state, piece)

    def place_piece(self, state, piece):
        return type.place_piece(state, piece)

    def move_valid(self, state, piece, x_to, y_to):

        return piece and self.in_bounds(piece.x, piece.y) and \
            self.in_bounds(x_to, y_to) and \
            piece.owner == state.turn.current and\
            (x_to != piece.x or y_to != piece.y) and\
            not state.friendly(x_to, y_to) and\
            piece.type.move_valid(state, piece, x_to, y_to)

    def move_piece(self, state, piece, x_to, y_to):
        return piece.type.move_piece(state, piece, x_to, y_to)

    def remove_valid(self, state, piece):
        return piece and self.in_bounds(piece.x, piece.y) and\
            piece.type.remove_valid(state, piece)

    def remove_piece(self, state, piece):
        return piece.type.remove_piece(state, piece)

    def moveable(self, state, piece):
        return piece and piece.owner == state.turn.current and\
               piece.type.moveable(state, piece)

    def input(self, state, input, contr):

        for action in self.actions:
            if isinstance(input, action.input):
                result, contr = action.apply(state, input, contr)
                if result: return result, contr
        return None, contr

    def setup(self):

        players = [PlayerState(order=i, score=0)
            for i in range(0, self.players)]

        pieces = [[self.piece(x, y)
            for y in range(0, self.height)]
                for x in range(0, self.width)]

        turn = Turn(current=0, stage=0, ply=0)
        outcome = Outcome(finished=False, winner=None, draw=False)

        return State(game=self, players=players, pieces=pieces,
            turn=turn, outcome=outcome, previous=None)

    def piece(self, x, y):
        return None

    def texture(self, state, x, y):
        piece = state.pieces[x][y]
        if piece: return piece.type.texture(piece.owner)
        else: return None

    def scale(self, x, y):
        return 1, 1

    def colour(self, state, x, y, contr):
        if contr.is_selected(x, y): return self.selected_colour
        #if state.modified(x, y): return self.modified
        #else: return self.background(x, y)
        else: return self.background(x, y)

    def background(self, x, y):
        if (x + y) % 2 == 0: return '#FDCB6E'
        else: return '#FFEAA7'

    selected_colour = '#6A89CC'
    modified_colour = '#74B9FF'

class PieceType:

    def texture(self, owner):
        return 'games/img/empty.png'

    def place_valid(self, state, piece):
        return False

    def place_piece(self, state, piece):
        return state.place_piece(piece).end_turn()

    def move_valid(self, state, piece, x_to, y_to):
        return False

    def move_piece(self, state, piece, x_to, y_to):
        return state.move_piece(piece, x_to, y_to).end_turn()

    def remove_valid(self, state, piece):
        return False

    def remove_piece(self, state, piece):
        return state.remove_piece(piece).end_turn()

    def moveable(self, state, piece):
        return True