from games.games.common.input import *
from games.games.common.state import *

class PlaceAction:

    input = BoardInput

    def __init__(self, type):
        self.type = type

    def apply(self, state, display, input):

        clicked = Piece(self.type, state.turn.current, input.x, input.y)

        if state.game.place_valid(state, clicked):
            result = state.game.place_piece(state.clear_changes(), clicked)
            return result, display

        return None, display

    def display(self, state, display):

        for x in range(0, state.game.width):
            for y in range(0, state.game.height):

                piece = Piece(self.type, state.turn.current, x, y)
                if state.game.place_valid(state, piece):
                    texture = self.type.texture(state.turn.current)
                    display = display.add_texture(x, y, Texture(texture, 0.2))\
                        .add_texture(x, y, state.game.place_icon)

        return display

class MoveAction:

    input = BoardInput

    def apply(self, state, display, input):

        clicked = state.pieces[input.x][input.y]

        if len(display.selections) > 0:
            pos = display.selections[0]
            selected = state.pieces[pos[0]][pos[1]]

            if state.game.move_valid(state, selected, input.x, input.y):
                result = state.game.move_piece(
                    state.clear_changes(), selected, input.x, input.y)
                return result, display.clear_selections()

        if state.game.moveable(state, clicked):
            return None, display.clear_selections().select(input.x, input.y)

        return None, display.clear_selections()

    def display(self, state, display):

        if len(display.selections) > 0:
            pos = display.selections[0]
            selected = state.pieces[pos[0]][pos[1]]

            for x in range(0, state.game.width):
                for y in range(0, state.game.height):

                    if state.game.move_valid(state, selected, x, y):
                        texture = state.game.attack_icon if state.enemy(x, y) else\
                            Texture(selected.type.texture(state.turn.current), 0.2)
                        display = display.add_texture(x, y, texture)

        return display

class RemoveAction:

    input = BoardInput

    def apply(self, state, display, input):

        clicked = state.pieces[input.x][input.y]

        if state.game.remove_valid(state, clicked):
            result = state.game.remove_piece(state.clear_changes(), clicked)
            return result, display

        return None, display

    def display(self, state, display):

        for x in range(0, state.game.width):
            for y in range(0, state.game.height):

                if state.game.remove_valid(state, state.pieces[x][y]):
                    display = display.add_texture(x, y, state.game.attack_icon)\
                        .enable_buffering(x, y)

        return display