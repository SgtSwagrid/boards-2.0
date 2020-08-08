from games.games.common.action import *
from games.games.common.display import *
from games.games.common.event import *
from games.games.common.state import *


ATTACK_ICON = [Texture('common/attack.png', 0.8)]
PLACE_ICON = [Texture('common/place.png', 0.8)]

class Handler:

    event = BoardEvent

    def apply(self, state, event):
        return False, None, DisplayProperties()

    def texture(self, state, display, x, y):
        return []

class PlaceHandler(Handler):

    def __init__(self, type, hints=True, icon=PLACE_ICON):
        self.type = type
        self.hints = hints
        self.icon = icon

    def apply(self, state, event):

        clicked = Piece(self.type, state.turn.current_id, event.x, event.y)
        action = PlaceAction(clicked)

        if action.validate(state):
            result = action.apply(state)
            return True, result, DisplayProperties()

        return False, None, DisplayProperties()

    def texture(self, state, event, x, y):

        if self.hints:

            piece = Piece(self.type, state.turn.current_id, x, y)

            if PlaceAction(piece).validate(state):
                return [t.set_opacity(0.2) for t in
                    piece.type.texture(piece, state)] + self.icon

        return []

class MoveHandler(Handler):

    def __init__(self, hints=True, icon=ATTACK_ICON):
        self.hints = hints
        self.icon = icon

    def apply(self, state, event):

        clicked = state.pieces[event.x][event.y]

        if len(event.properties.selections) > 0:
            pos = event.properties.selections[0]
            selected = state.pieces[pos[0]][pos[1]]

            action = MoveAction(selected, event.x, event.y)
            if action.validate(state):
                result = action.apply(state)
                return True, result, DisplayProperties()

        if state.game.moveable(state, clicked):
            selections = [(event.x, event.y)]
            return True, None, DisplayProperties(selections)

        return False, None, DisplayProperties()

    def texture(self, state, event, x, y):

        if self.hints:

            if len(event.properties.selections) > 0:

                pos = event.properties.first_selection()
                selected = state.pieces[pos[0]][pos[1]]

                if MoveAction(selected, x, y).validate(state):

                    if state.enemy(x, y): return self.icon
                    else: return [t.set_opacity(0.2) for t in
                        selected.type.texture(selected, state)]

        return []

class RemoveHandler(Handler):

    def __init__(self, hints=False, icon=ATTACK_ICON):
        self.hints = hints
        self.icon = icon

    def apply(self, state, event):

        clicked = state.pieces[event.x][event.y]
        action = RemoveAction(clicked)

        if action.validate(state):
            result = action.apply(state)
            return True, result, DisplayProperties()

        return False, None, DisplayProperties()

    def texture(self, state, event, x, y):

        if self.hints:

            if RemoveAction(state.pieces[x][y]).validate(state):
                return self.icon

        return []
