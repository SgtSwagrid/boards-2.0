class Event:

    def __init__(self, properties, player_id, active):
        self.properties = properties
        self.player_id = player_id
        self.active = active

class BoardEvent(Event):

    def __init__(self, properties, player_id, active, x, y):
        super().__init__(properties, player_id, active)
        self.x = x
        self.y = y

class SelectEvent(Event):

    def __init__(self, properties, player_id, active, option_id, x, y):
        super().__init__(properties, player_id, active)
        self.option_id = option_id
        self.x = x
        self.y = y

class RenderEvent(Event):

    def __init__(self, properties, player_id, active):
        super().__init__(properties, player_id, active)

class DisplayProperties:

    def __init__(self, selections=[]):
        self.selections = selections

    def first_selection(self):
        return self.selections[0] if len(self.selections) > 0 else (-1, -1)

    def selected(self, x, y):
        return any((x, y) == s for s in self.selections)

    def get_selection(self, state, id):

        if 0 <= id < len(self.selections):
            pos = self.selections[id]
            if state.game.SHAPE.in_bounds(pos[0], pos[1]):
                return state.pieces[pos[0]][pos[1]]