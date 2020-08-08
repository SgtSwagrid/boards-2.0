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