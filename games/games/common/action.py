class Action:

    def validate(self, state):
        return False

    def apply(self, state):
        return state

class PlaceAction(Action):

    def __init__(self, piece):
        self.piece = piece

    def validate(self, state):
        return state.game.place_valid(state, self.piece)

    def apply(self, state):
        state = state.push_action(self)
        state = state.game.place_piece(state, self.piece)
        return state.set_outcome(state.game.outcome(state))

class MoveAction(Action):

    def __init__(self, piece, x_to, y_to):
        self.piece = piece
        self.x_to = x_to
        self.y_to = y_to

    def validate(self, state):
        return state.game.move_valid(state,
            self.piece, self.x_to, self.y_to)

    def apply(self, state):
        state = state.push_action(self)
        state = state.game.move_piece(state, self.piece, self.x_to, self.y_to)
        return state.set_outcome(state.game.outcome(state))

class RemoveAction(Action):

    def __init__(self, piece):
        self.piece = piece

    def validate(self, state):
        return state.game.remove_valid(state, self.piece)

    def apply(self, state):
        state = state.push_action(self)
        state = state.game.remove_piece(state, self.piece)
        return state.set_outcome(state.game.outcome(state))