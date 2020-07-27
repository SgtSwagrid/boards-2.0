from games.games.common.input import ClickInput
from games.games.common.state import Piece

class PlaceAction:

    input = ClickInput

    def __init__(self, type):
        self.type = type

    def apply(self, state, input, contr):

        clicked = Piece(self.type, state.turn.current, input.x, input.y)

        if state.game.place_valid(state, clicked):
            result = state.game.place_piece(state, clicked)
            return result, contr

        return None, contr

class MoveAction:

    input = ClickInput

    def apply(self, state, input, contr):

        clicked = state.pieces[input.x][input.y]

        if contr.num_selected() == 1:

            selected_pos = contr.first_selected()
            selected = state.pieces[selected_pos[0]][selected_pos[1]]

            if state.game.move_valid(state, selected, input.x, input.y):
                result = state.game.move_piece(state, selected, input.x, input.y)
                return result, contr.clear()

        if state.game.moveable(state, clicked):
            return None, contr.clear().select(input.x, input.y)

        return None, contr.clear()

class RemoveAction:

    input = ClickInput

    def apply(self, state, input, contr):

        clicked = state.pieces[input.x][input.y]

        if state.game.remove_valid(state, clicked):
            result = state.game.remove_piece(state, clicked)
            return result, contr

        return None, contr