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

    def disable_board(self, state, event):
        return False


class PlaceHandler(Handler):

    EVENTS = [BoardEvent]

    def __init__(self, type, hints=True, icon=PLACE_ICON,
            can_capture_self=False, can_capture_enemy=False):

        self.type = type
        self.hints = hints
        self.icon = icon
        self.can_capture_self = can_capture_self
        self.can_capture_enemy = can_capture_enemy

    def apply(self, state, event):

        in_bounds = state.game.SHAPE.in_bounds(event.x, event.y)
        piece = Piece(self.type, state.turn.current_id, event.x, event.y)

        if in_bounds and event.active and self.place_valid(state, piece):

            state = state.push_action(PlaceAction(piece))
            state = self.place_piece(state, piece)
            return True, state, DisplayProperties()

        return False, None, None

    def texture(self, state, event, x, y):

        if self.hints and event.active and state.game.board_enabled(state, event):

            piece = Piece(self.type, state.turn.current_id, x, y)

            if self.place_valid(state, piece):
                return [t.set_opacity(0.2) for t in
                    piece.type.texture(piece, state)] + self.icon

        return []

    def place_valid(self, state, piece):

        return state.game.SHAPE.in_bounds(piece.x, piece.y) and\
            piece.owner_id == state.turn.current_id and\
            not state.pieces[piece.x][piece.y] and \
            (self.can_capture_self or not state.friendly(piece.x, piece.y)) and\
            (self.can_capture_enemy or not state.enemy(piece.x, piece.y)) and\
            piece.type.place_valid(state, piece)

    def place_piece(self, state, piece):

        return piece.type.place_piece(state, piece)


class MoveHandler(Handler):

    EVENTS = [BoardEvent]

    def __init__(self, types=[], hints=True, icon=ATTACK_ICON,
            can_capture_self=False, can_capture_enemy=True):

        self.types = types
        self.hints = hints
        self.icon = icon
        self.can_capture_self=can_capture_self
        self.can_capture_enemy=can_capture_enemy

    def apply(self, state, event):

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

        if self.hints and event.active and state.game.board_enabled(state, event):

            selected = event.properties.get_selection(state, 0)

            if selected and self.move_valid(state, selected, x, y):

                if state.enemy(x, y): return self.icon
                else: return [t.set_opacity(0.2) for t in
                    selected.type.texture(selected, state)]

        return []

    def move_valid(self, state, piece, x_to, y_to):

        return state.game.SHAPE.in_bounds(x_to, y_to) and\
            piece.owner_id == state.turn.current_id and\
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

    EVENTS = [BoardEvent]

    def __init__(self, types=[], hints=True, icon=ATTACK_ICON,
            can_capture_self=True, can_capture_enemy=True):

        self.types = types
        self.hints = hints
        self.icon = icon
        self.can_capture_self = can_capture_self
        self.can_capture_enemy = can_capture_enemy

    def apply(self, state, event):

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

        if self.hints and event.active and state.game.board_enabled(state, event):

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

    EVENTS = [SelectEvent]

    def apply(self, state, event):

        if self.show(state, event) and 0 <= event.option_id\
                < len((selector := self.selector(state, event)).options):

            state = state.push_action(SelectAction(event.option_id))
            state = self.select(state, event, selector.options[event.option_id])
            return True, state, DisplayProperties()

        return False, None, None

    def render(self, state, event, display):

        if event.active and self.show(state, event):
            return display.show_selector(self.selector(state, event))

        return display

    def disable_board(self, state, event):
        return self.show(state, event)

    def show(self, state, event):
        return False

    def selector(self, state, event):
        return None

    def select(self, state, event, option):
        return state


class MultiPlaceHandler(PlaceHandler, SelectHandler):

    EVENTS = [BoardEvent, SelectEvent]

    def __init__(self, types, shape, hints=True, icon=PLACE_ICON,
            can_capture_self=False, can_capture_enemy=False):

        super().__init__(None, hints, icon,
            can_capture_self, can_capture_enemy)
        self.types = types
        self.shape = shape

    def apply(self, state, event):

        if isinstance(event, BoardEvent):

            in_bounds = state.game.SHAPE.in_bounds(event.x, event.y)
            placeable = self.placeable(state, event.x, event.y)

            if event.properties.first_selection() == (event.x, event.y):
                return True, None, DisplayProperties()

            elif in_bounds and event.active and any(placeable):
                return True, None, DisplayProperties([(event.x, event.y)])

        elif isinstance(event, SelectEvent):
            return SelectHandler.apply(self, state, event)

        return False, None, None

    def texture(self, state, event, x, y):

        if self.hints and event.active and state.game.board_enabled(state, event):

            if any(self.placeable(state, x, y)):
                return self.icon

        return []

    def placeable(self, state, x, y):

        pieces = [Piece(t, state.turn.current_id, x, y) for t in self.types]
        return [p for p in pieces if self.place_valid(state, p)]

    def show(self, state, event):

        x, y = event.properties.first_selection()
        return any(self.placeable(state, x, y))

    def selector(self, state, event):

        x, y = event.properties.first_selection()
        placeable = self.placeable(state, x, y)
        return PieceSelector(placeable, state, x, y, self.shape)

    def select(self, state, event, option):

        x, y = event.properties.first_selection()
        type = state.game.PIECES[option.value]
        piece = Piece(type, state.turn.current_id, x, y)
        return self.place_piece(state, piece)

    def disable_board(self, state, event):
        return False
