from games.games.common.actions import *
from games.games.common.display import *
from games.games.common.events import *
from games.games.common.state import *


ATTACK_ICON = [Texture('common/attack.png', 0.8)]
PLACE_ICON = [Texture('common/place.png', 0.8)]


class Handler:

    def apply(self, state, event):
        return False, None, DisplayProperties()

    def actions(self, state):
        return []

    def render(self, state, event, display):
        return display

    def texture(self, state, event, x, y):
        return []


class PlaceHandler(Handler):

    EVENTS = [BoardEvent]

    def __init__(self, type, hints=True, icon=PLACE_ICON,
            capture_self=False, capture_enemy=False):

        self.type = type
        self.hints = hints
        self.icon = icon
        self.capture_self = capture_self
        self.capture_enemy = capture_enemy

    def apply(self, state, event):

        piece = Piece(self.type, state.turn.current_id, event.x, event.y)

        if piece.type.ID == self.type.ID and\
                self.place_valid(state, piece):

            state = self.place_piece(state, piece)
            return True, state, DisplayProperties()

        return False, None, None

    def actions(self, state):

        pieces = [Piece(self.type, state.turn.current_id, x, y)
            for y in range(0, state.game.SHAPE.height)
            for x in range(0, state.game.SHAPE.row_size(y))]

        return [PlaceAction(piece) for piece in pieces
            if self.place_valid(state, piece)]

    def texture(self, state, event, x, y):

        if self.hints and event.active:

            piece = Piece(self.type, state.turn.current_id, x, y)

            if self.place_valid(state, piece):
                return [t.set_opacity(0.2) for t in
                    piece.type.texture(piece, state)] + self.icon

        return []

    def place_valid(self, state, piece):

        return state.game.SHAPE.in_bounds(piece.x, piece.y) and\
            piece.owner_id == state.turn.current_id and\
            (self.capture_self or not state.friendly(piece.x, piece.y)) and\
            (self.capture_enemy or not state.enemy(piece.x, piece.y)) and\
            piece.type.place_valid(state, piece)

    def place_piece(self, state, piece):

        state = state.push_action(PlaceAction(piece))
        return piece.type.place_piece(state, piece)


class MoveHandler(Handler):

    EVENTS = [BoardEvent]

    def __init__(self, types=[], hints=True, icon=ATTACK_ICON,
            capture_self=False, capture_enemy=True):

        self.types = types
        self.hints = hints
        self.icon = icon
        self.capture_self=capture_self
        self.capture_enemy=capture_enemy

    def apply(self, state, event):

        clicked = state.pieces[event.x][event.y]
        selected = event.properties.get_selection(state, 0)

        if selected == clicked:
            return False, None, None

        elif selected and any(selected.type.ID == t.ID for t in self.types) and\
                self.move_valid(state, selected, event.x, event.y):

            state = state.push_action(MoveAction(selected, event.x, event.y))
            state = self.move_piece(state, selected, event.x, event.y)
            return True, state, DisplayProperties()

        elif clicked and self.moveable(state, clicked):
            return True, None, DisplayProperties([(event.x, event.y)])

        return False, None, None

    def actions(self, state):

        return [MoveAction(piece, x, y)
            for piece in state.find_pieces()
            if piece.type in self.types
            for y in range(0, state.game.SHAPE.height)
            for x in range(0, state.game.SHAPE.row_size(y))
            if self.move_valid(state, piece, x, y)]

    def texture(self, state, event, x, y):

        if self.hints and event.active:

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
            (self.capture_self or not state.friendly(x_to, y_to)) and\
            (self.capture_enemy or not state.enemy(x_to, y_to)) and\
            piece.type.move_valid(state, piece, x_to, y_to)

    def move_piece(self, state, piece, x_to, y_to):

        state = state.push_action(MoveAction(piece, x_to, y_to))
        return piece.type.move_piece(state, piece, x_to, y_to)

    def moveable(self, state, piece):

        return any(self.move_valid(state, piece, x, y)
            for y in range(0, state.game.SHAPE.height)
            for x in range(0, state.game.SHAPE.row_size(y)))


class RemoveHandler(Handler):

    EVENTS = [BoardEvent]

    def __init__(self, types=[], hints=True, icon=ATTACK_ICON,
            capture_self=True, capture_enemy=True):

        self.types = types
        self.hints = hints
        self.icon = icon
        self.capture_self = capture_self
        self.capture_enemy = capture_enemy

    def apply(self, state, event):

        piece = state.pieces[event.x][event.y]

        if piece and any(piece.type.ID == t.ID for t in self.types) and\
                self.remove_valid(state, piece):

            state = state.push_action(RemoveAction(piece))
            state = self.remove_piece(state, piece)
            return True, state, DisplayProperties()

        return False, None, DisplayProperties()

    def actions(self, state):

        return [RemoveAction(piece)
            for piece in state.find_pieces()
            if piece.type in self.types
            if self.remove_valid(state, piece)]

    def texture(self, state, event, x, y):

        if self.hints and event.active:

            piece = state.pieces[x][y]

            if piece and self.remove_valid(piece):
                return self.icon

        return []

    def remove_valid(self, state, piece):

        return (self.capture_self or piece.ownerId != state.turn.current) and\
            (self.capture_enemy or piece.ownerId == state.turn.current) and\
            piece.type.remove_valid(state, piece)

    def remove_piece(self, state, piece):

        state = state.push_action(RemoveAction(piece))
        return piece.type.remove_piece(state, piece)


class SelectHandler(Handler):

    EVENTS = [SelectEvent, BoardEvent]

    def __init__(self, click_to_show=False, hints=False, icon=PLACE_ICON):
        self.click_to_show = click_to_show
        self.hints = hints
        self.icon = icon

    def apply(self, state, event):

        enabled = self.enabled(state, event.x, event.y)
        options = self.options(state, event.x, event.y)\
            if enabled else []

        if isinstance(event, BoardEvent) and self.click_to_show:

            if event.properties.selected(event.x, event.y):
                return True, None, DisplayProperties()

            elif enabled:
                return True, None, DisplayProperties([(event.x, event.y)])

        elif isinstance(event, SelectEvent) and enabled and\
                0 <= event.option_id < len(options):

            state = state.push_action(SelectAction(
                event.option_id, event.x, event.y))

            state = self.select(state,
                options[event.option_id], event.x, event.y)

            return True, state, DisplayProperties()

        return False, None, None

    def actions(self, state):

        return [SelectAction(option.id, x, y)
            for y in range(0, state.game.SHAPE.height)
            for x in range(0, state.game.SHAPE.row_size(y))
            if self.enabled(state, x, y)
            for option in self.options(state, x, y)]

    def render(self, state, event, display):

        if not event.active: return display

        selectors = [self.selector(state, self.options(state, x, y), x, y)
            for y in range(0, state.game.SHAPE.height)
            for x in range(0, state.game.SHAPE.row_size(y))
            if self.visible(state, event, x, y)]

        return display.add_selectors(selectors)

    def texture(self, state, event, x, y):

        if self.hints and event.active and self.enabled(state, x, y) and\
                not self.visible(state, event, x, y):
            return self.icon

        return []

    def visible(self, state, event, x, y):

        return self.enabled(state, x, y) and\
            any(self.options(state, x, y)) and\
            (not self.click_to_show or event.properties.selected(x, y))

    def enabled(self, state, x, y):
        return any(self.options(state, x, y))

    def options(self, state, x, y):
        return []

    def selector(self, state, options, x, y):
        return Selector(options, x, y, state)

    def select(self, state, option, x, y):
        return state.push_action(SelectAction(option.id, x, y))


class MultiPlaceHandler(SelectHandler, PlaceHandler):

    def __init__(self, types=[], hints=True, icon=PLACE_ICON,
            capture_self=True, capture_enemy=True, click_to_show=True):

        SelectHandler.__init__(self, click_to_show, icon)

        PlaceHandler.__init__(self, None, hints, icon,
            capture_self, capture_enemy)

        self.types = types

    def actions(self, state):

        pieces = [Piece(type, state.turn.current_id, x, y)
            for y in range(0, state.game.SHAPE.height)
            for x in range(0, state.game.SHAPE.row_size(y))
            if self.enabled(state, x, y)
            for type in self.pieces(state, x, y)]

        return [PlaceAction(piece) for piece in pieces
            if self.place_valid(state, piece)]

    def options(self, state, x, y):

        pieces = [Piece(type, state.turn.current_id, x, y)
            for type in self.pieces(state, x, y)]

        return [Option(i, piece.type.ID, piece.type.texture(piece, state))
            for i, piece in enumerate(pieces)]

    def pieces(self, state, target_x, target_y):

        pieces = [Piece(t, state.turn.current_id, target_x, target_y)
            for t in self.types]

        return [piece.type for piece in pieces
            if self.place_valid(state, piece)]

    def select(self, state, option, target_x, target_y):

        piece = Piece(state.game.PIECES[option.value],
            state.turn.current_id, target_x, target_y)

        state = state.push_action(PlaceAction(piece))
        return state.place_piece(piece)
