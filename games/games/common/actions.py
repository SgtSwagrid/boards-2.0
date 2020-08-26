class PlaceAction:

    def __init__(self, piece, new_pos):

        self.piece = piece
        self.new_pos = new_pos


class MoveAction:

    def __init__(self, piece, old_pos, new_pos):

        self.piece = piece.at(new_pos)
        self.old_pos = old_pos
        self.new_pos = new_pos


class RemoveAction:

    def __init__(self, piece, old_pos):

        self.piece = piece
        self.old_pos = old_pos


class SelectAction:

    def __init__(self, option_id, target):

        self.option_id = option_id
        self.target = target
