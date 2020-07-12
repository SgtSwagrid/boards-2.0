class Game:

    types = []

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def exists(self, pieces, x, y):
        return self.in_bounds(x, y) and pieces[x][y]

    def mine(self, state, pieces, x, y):
        return self.exists(pieces, x, y) and\
               pieces[x][y].owner_id == state.turn

    def enemy(self, state, pieces, x, y):
        return self.exists(pieces, x, y) and\
               pieces[x][y].owner_id != state.turn

    def place_valid(self, state, pieces, type, owner_id, x, y):
        return self.in_bounds(x, y) and \
               owner_id == state.turn and \
               type.place_valid(state, pieces, owner_id, x, y)

    def place_piece(self, state, pieces, type, owner_id, x, y):
        type.place_piece(state, pieces, owner_id, x, y)

    def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):
        return self.mine(state, pieces, x_from, y_from) and\
               self.in_bounds(x_to, y_to) and\
               (x_to != x_from or y_to != y_from) and\
               pieces[x_from][y_from].type().move_valid(
                   state, pieces, x_from, y_from, x_to, y_to)

    def move_piece(self, state, pieces, x_from, y_from, x_to, y_to):
        pieces[x_from][y_from].type()\
            .move_piece(state, pieces, x_from, y_from, x_to, y_to)

    def remove_valid(self, state, pieces, x, y):
        return self.exists(pieces, x, y) and\
               pieces[x][y].type().remove_valid(state, pieces, x, y)

    def remove_piece(self, state, pieces, x, y):
        pieces[x][y].type().remove_piece(state, pieces, x, y)

    def selectable(self, state, pieces, x, y):
        return self.mine(state, pieces, x, y) and\
               pieces[x][y].type().selectable(state, pieces, x, y)

    def initial(self, x, y):
        return None, 0

    def scale(self, x, y):
        return 1, 1

    def colour(self, state, pieces, x, y):
        return self.background(x, y)

    def background(self, x, y):
        if (x + y) % 2 == 0: return '#FDCB6E'
        else: return '#FFEAA7'

    highlight = '#6A89CC'

class Piece:

    def place_valid(self, state, pieces, owner_id, x, y):
        return False

    def place_piece(self, state, pieces, owner_id, x, y):
        state.place_piece(self, owner_id, x, y)
        state.end_turn()

    def move_valid(self, state, pieces, x_from, y_from, x_to, y_to):
        return False

    def move_piece(self, state, pieces, x_from, y_from, x_to, y_to):
        state.move_piece(x_from, y_from, x_to, y_to)
        state.end_turn()

    def remove_valid(self, state, pieces, x, y):
        return False

    def remove_piece(self, state, pieces, x, y):
        state.remove_piece(x, y)
        state.end_turn()

    def selectable(self, state, pieces, x, y):
        return False