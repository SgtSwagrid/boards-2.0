from games.games.common.actions import *
from games.games.common.display import *
from games.games.common.events import *
from games.games.common.state import *


ATTACK_ICON = [Texture('common/attack.png', 0.8)]
PLACE_ICON = [Texture('common/place.png', 0.8)]


class Handler:

    def apply(self, state, event):
        return False, None, DisplayProperties()

    def texture(self, state, display, x, y):
        return []

    def render(self, state, event, display):
        return display

    def board_enabled(self, state):
        return True


class PlaceHandler(Handler):

    EVENT = BoardEvent

    def __init__(self, type, hints=True, icon=PLACE_ICON,
            can_capture_self=False, can_capture_enemy=False):

        self.type = type
        self.hints = hints
        self.icon = icon
        self.can_capture_self = can_capture_self
        self.can_capture_enemy = can_capture_enemy

    def apply(self, state, event):

        if not state.game.board_enabled(state): return False, None, None

        in_bounds = state.game.SHAPE.in_bounds(event.x, event.y)
        piece = Piece(self.type, state.turn.current_id, event.x, event.y)

        if in_bounds and event.active and self.place_valid(state, piece):

            state = state.push_action(PlaceAction(piece))
            state = self.place_piece(state, piece)
            return True, state, DisplayProperties()

        return False, None, None

    def texture(self, state, event, x, y):

        if self.hints and event.active and state.game.board_enabled(state):

            piece = Piece(self.type, state.turn.current_id, x, y)

            if self.place_valid(state, piece):
                return [t.set_opacity(0.2) for t in
                    piece.type.texture(piece, state)] + self.icon

        return []

    def place_valid(self, state, piece):

        return piece.owner_id == state.turn.current_id and\
            not state.pieces[piece.x][piece.y] and \
            (self.can_capture_self or not state.friendly(piece.x, piece.y)) and\
            (self.can_capture_enemy or not state.enemy(piece.x, piece.y)) and\
            piece.type.place_valid(state, piece)

    def place_piece(self, state, piece):

        return piece.type.place_piece(state, piece)


class MoveHandler(Handler):

    EVENT = BoardEvent

    def __init__(self, types=[], hints=True, icon=ATTACK_ICON,
            can_capture_self=False, can_capture_enemy=True):

        self.types = types
        self.hints = hints
        self.icon = icon
        self.can_capture_self=can_capture_self
        self.can_capture_enemy=can_capture_enemy

    def apply(self, state, event):

        if not state.game.board_enabled(state): return False, None, None

        in_bounds = state.game.SHAPE.in_bounds(event.x, event.y)
        clicked = state.pieces[event.x][event.y] if in_bounds else None
        selected = event.properties.get_selection(state, 0)

        if selected == clicked:
            return False, None, None

        elif selected and in_bounds and event.active and\
                any(selected.type.ID == t.ID for t in self.types) and\
                self.move_valid(state, selected, event.x, event.y):

            state = state.push_action(MoveAction(selected, event.x, event.y))
            state = self.move_piece(state, selected, event.x, event.y)
            return True, state, DisplayProperties()

        elif clicked and self.moveable(state, clicked):
            return True, None, DisplayProperties([(event.x, event.y)])

        return False, None, None

    def texture(self, state, event, x, y):

        if self.hints and event.active and state.game.board_enabled(state):

            selected = event.properties.get_selection(state, 0)

            if selected and self.move_valid(state, selected, x, y):

                if state.enemy(x, y): return self.icon
                else: return [t.set_opacity(0.2) for t in
                    selected.type.texture(selected, state)]

        return []

    def move_valid(self, state, piece, x_to, y_to):

        return piece.owner_id == state.turn.current_id and\
            (x_to != piece.x or y_to != piece.y) and\
            (self.can_capture_self or not state.friendly(x_to, y_to)) and\
            (self.can_capture_enemy or not state.enemy(x_to, y_to)) and\
            piece.type.move_valid(state, piece, x_to, y_to)

    def move_piece(self, state, piece, x_to, y_to):

        return piece.type.move_piece(state, piece, x_to, y_to)

    def moveable(self, state, piece):

        return any(self.move_valid(state, piece, x, y)
            for y in range(0, state.game.SHAPE.height)
            for x in range(0, state.game.SHAPE.row_size(y)))


class RemoveHandler(Handler):

    EVENT = BoardEvent

    def __init__(self, types=[], hints=True, icon=ATTACK_ICON,
            can_capture_self=True, can_capture_enemy=True):

        self.types = types
        self.hints = hints
        self.icon = icon
        self.can_capture_self = can_capture_self
        self.can_capture_enemy = can_capture_enemy

    def apply(self, state, event):

        if not state.game.board_enabled(state): return False, None, None

        in_bounds = state.game.SHAPE.in_bounds(event.x, event.y)
        piece = state.pieces[event.x][event.y] if in_bounds else None

        if piece and event.active and\
                any(piece.type.ID == t.ID for t in self.types) and\
                self.remove_valid(state, piece):

            state = state.push_action(RemoveAction(piece))
            state = self.remove_piece(state, piece)
            return True, state, DisplayProperties()

        return False, None, DisplayProperties()

    def texture(self, state, event, x, y):

        if self.hints and event.active and state.game.board_enabled(state):

            piece = state.pieces[x][y]

            if piece and self.remove_valid(piece):
                return self.icon

        return []

    def remove_valid(self, state, piece):

        return (self.can_capture_self or piece.ownerId != state.turn.current) and\
            (self.can_capture_enemy or piece.ownerId == state.turn.current) and\
            piece.type.remove_valid(state, piece)

    def remove_piece(self, state, piece):

        return piece.type.remove_piece(state, piece)


class SelectHandler(Handler):

    EVENT = SelectEvent

    def apply(self, state, event):

        if self.show(state) and 0 <= event.option_id\
                < len((selector := self.selector(state)).options):

            state = state.push_action(SelectAction(event.option_id))
            state = self.select(state, selector.options[event.option_id])
            return True, state, DisplayProperties()

        return False, None, None

    def render(self, state, event, display):

        if event.active and self.show(state):
            return display.show_selector(self.selector(state))

        return display

    def board_enabled(self, state):
        return not self.show(state)

    def show(self, state):
        return False

    def selector(self, state):
        return None

    def select(self, state, option):
        return state
