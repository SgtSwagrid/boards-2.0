import copy

class Action:

    def __init__(self, changes=[]):
        self.changes=changes

    def validate(self, state):
        return False

    def apply(self, state):
        return state.push_action(self)

    def set_changed(self, change):
        action = copy.deepcopy(self)
        action.changes.append(change)
        return action

    def changed(self, x, y):
        return any((c.x, c.y) == (x, y) for c in self.changes)

class PlaceAction(Action):

    def __init__(self, piece, changes=[]):
        super().__init__(changes)
        self.piece = piece

    def validate(self, state):
        return state.game.place_valid(state, self.piece)

    def apply(self, state):
        return state.game.place_piece(super().apply(state), self.piece)

class MoveAction(Action):

    def __init__(self, piece, x_to, y_to, changes=[]):
        super().__init__(changes)
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

    def __init__(self, piece, changes=[]):
        super().__init__(changes)
        self.piece = piece

    def validate(self, state):
        return state.game.remove_valid(state, self.piece)

    def apply(self, state):
        return state.game.remove_piece(super().apply(state), self.piece)

class Change:

    def __init__(self, x, y, old, new):
        self.x = x
        self.y = y
        self.old = old
        self.new = new
