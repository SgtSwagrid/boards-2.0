class PlaceAction:

    def __init__(self, piece):
        self.piece = piece
        self.x_to = piece.x
        self.y_to = piece.y


class MoveAction:

    def __init__(self, piece, x_to, y_to):
        self.piece = piece
        self.x_from = piece.x
        self.y_from = piece.y
        self.x_to = x_to
        self.y_to = y_to


class RemoveAction:

    def __init__(self, piece):
        self.piece = piece
        self.x_from = piece.x
        self.y_from = piece.y


class SelectAction:

    def __init__(self, option_id, x_to, y_to):
        self.option_id = option_id
        self.x_to = x_to
        self.y_to = y_to
