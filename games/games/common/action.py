import copy

class Action:

    def __init__(self, changes=[]):
        self.changes=changes

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


class MoveAction(Action):

    def __init__(self, piece, x_from, y_from, changes=None):
        super().__init__(changes if changes else\
            [(x_from, y_from), (piece.x, piece.y)])
        self.piece = piece
        self.x_from = x_from
        self.y_from = y_from

class RemoveAction(Action):

    def __init__(self, piece, changes=None):
        super().__init__(changes if changes else [(piece.x, piece.y)])
        self.piece = piece
