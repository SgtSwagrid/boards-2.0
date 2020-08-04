from games.games.common.action import *
from games.games.common.input import *
from games.games.common.state import *

class Handler:

    event = BoardEvent

    def apply(self, state, display, event):
        return None, display

    def display(self, state, display):

        return display.add_textures([[self.texture(state, display, x, y)
            for y in range(0, state.game.height)]
            for x in range(0, state.game.width)])

class PlaceHandler(Handler):

    def __init__(self, type):
        self.type = type

    def apply(self, state, display, event):

        clicked = Piece(self.type, state.turn.current, event.x, event.y)
        action = PlaceAction(clicked)

        if action.validate(state):
            return action.apply(state), display

        return None, display

    def texture(self, state, display, x, y):

        piece = Piece(self.type, state.turn.current, x, y)

        if PlaceAction(piece).validate(state):
            texture = self.type.texture(piece, state, display)
            return [Texture(texture, 0.2), state.game.place_icon]

        return []

class MoveHandler(Handler):

    def apply(self, state, display, event):

        clicked = state.pieces[event.x][event.y]
        print(display.selections)

        if len(display.selections) > 0:
            pos = display.selections[0]
            selected = state.pieces[pos[0]][pos[1]]

            action = MoveAction(selected, event.x, event.y)
            if action.validate(state):
                return action.apply(state), display.clear_selections()

        if state.game.moveable(state, clicked):
            return None, display.clear_selections().select(event.x, event.y)

        return None, display.clear_selections()

    def texture(self, state, display, x, y):

        if len(display.selections) > 0:

            pos = display.selections[0]
            selected = state.pieces[pos[0]][pos[1]]

            if MoveAction(selected, x, y).validate(state):

                if state.enemy(x, y): return [state.game.attack_icon]
                else:
                    return [selected.type.texture(selected, state, display).set_opacity(0.2)]

        return []

class RemoveHandler(Handler):

    def apply(self, state, display, event):

        clicked = state.pieces[event.x][event.y]
        action = RemoveAction(clicked)

        if action.validate(state):
            return action.apply(state), display

        return None, display

    def texture(self, state, display, x, y):

        if RemoveAction(state.pieces[x][y]).validate(state):
            return [state.game.attack_icon]