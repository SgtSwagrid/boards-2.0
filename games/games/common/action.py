import copy

class Action:

    def __init__(self, changes=[]):
        self.changes=changes

    def validate(self, state):
        return False

    def apply(self, state):
        return state.push_action(self)

    def set_changed(self, x, y):
        action = copy.deepcopy(self)
        action.changes.append((x, y))
        return action

    def changed(self, x, y):
        return any(c == (x, y) for c in self.changes)

class PlaceAction(Action):

    def __init__(self, piece, changes=None):
        super().__init__(changes if changes else [(piece.x, piece.y)])
        self.piece = piece

    def validate(self, state):
        return state.game.place_valid(state, self.piece)

    def apply(self, state):
        return state.game.place_piece(super().apply(state), self.piece)

class MoveAction(Action):

    def __init__(self, piece, x_to, y_to, changes=None):
        super().__init__(changes if changes else\
            [(piece.x, piece.y), (x_to, y_to)])
        self.piece = piece
        self.x_to = x_to
        self.y_to = y_to

    def validate(self, state):
        return state.game.move_valid(state,
            self.piece, self.x_to, self.y_to)

    def apply(self, state):
        return state.game.move_piece(super().apply(state),
            self.piece, self.x_to, self.y_to)

class RemoveAction(Action):

    def __init__(self, piece, changes=None):
        super().__init__(changes if changes else [(piece.x, piece.y)])
        self.piece = piece

    def validate(self, state):
        return state.game.remove_valid(state, self.piece)

    def apply(self, state):
        return state.game.remove_piece(super().apply(state), self.piece)