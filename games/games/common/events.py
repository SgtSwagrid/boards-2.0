from .vector import *

class Event:

    def __init__(self, properties, player_id, active):
        self.properties = properties
        self.player_id = player_id
        self.active = active


class BoardEvent(Event):

    def __init__(self, properties, player_id, active, clicked):
        super().__init__(properties, player_id, active)
        self.clicked = clicked


class SelectEvent(Event):

    def __init__(self, properties, player_id, active, option_id, target):
        super().__init__(properties, player_id, active)
        self.option_id = option_id
        self.target = target


class RenderEvent(Event):

    def __init__(self, properties, player_id, active):
        super().__init__(properties, player_id, active)


class DisplayProperties:

    def __init__(self, selections=[]):
        self.selected = selections

    def selection(self):
        return self.selected[0] if len(self.selected) > 0 else Vec(-1, -1)

    def is_selected(self, pos):
        return any(pos == s for s in self.selected)

    def get_piece(self, state, id):

        if 0 <= id < len(self.selected):
            pos = self.selected[id]
            if state.game.SHAPE.in_bounds(pos):
                return state.piece(pos)
