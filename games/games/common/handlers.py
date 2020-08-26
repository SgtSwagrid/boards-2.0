from games.games.common.actions import *
from games.games.common.display import *
from games.games.common.events import *
from games.games.common.kernels import *
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

    def texture(self, state, event, pos):
        return []


class PlaceHandler(Handler):

    EVENTS = [BoardEvent]

    def __init__(self, type, hints=True, icon=PLACE_ICON, stage=-1,
            capture_self=False, capture_enemy=False):

        self.type = type
        self.hints = hints
        self.icon = icon
        self.stage = stage
        self.capture_self = capture_self
        self.capture_enemy = capture_enemy

    def apply(self, state, event):

        piece = Piece(self.type, state.turn.current_id, event.clicked)

        if piece.type.ID == self.type.ID and\
                self.place_valid(state, piece):

            state = self.place_piece(state, piece)\
                .push_action(PlaceAction(piece))
            return True, state, DisplayProperties()

        return False, None, None

    def actions(self, state):

        pieces = [Piece(self.type, state.turn.current_id, pos)
            for pos in state.game.SHAPE.positions()]

        return [PlaceAction(piece) for piece in pieces
            if self.place_valid(state, piece)]

    def texture(self, state, event, pos):

        if self.hints and event.active:

            piece = Piece(self.type, state.turn.current_id, pos)

            if self.place_valid(state, piece):
                return [t.set_opacity(0.2) for t in
                    piece.type.texture(piece, state)] + self.icon

        return []

    def place_valid(self, state, piece):

        return state.game.SHAPE.in_bounds(piece.pos) and\
            piece.owner_id == state.turn.current_id and\
            (self.stage in [-1, state.turn.stage]) and\
            (self.capture_self or not state.friendly(piece.pos)) and\
            (self.capture_enemy or not state.enemy(piece.pos)) and\
            piece.type.place_valid(state, piece)

    def place_piece(self, state, piece):

        return piece.type.place_piece(state, piece)


class MoveHandler(Handler):

    EVENTS = [BoardEvent]

    def __init__(self, types=[], hints=True, icon=ATTACK_ICON, stage=-1,
            capture_self=False, capture_enemy=True,
            move_enemy=False, allow_jumps=True):

        self.types = types
        self.hints = hints
        self.icon = icon
        self.stage = stage
        self.capture_self = capture_self
        self.capture_enemy = capture_enemy
        self.move_enemy = move_enemy
        self.allow_jumps = allow_jumps

    def apply(self, state, event):

        clicked = state.piece(event.clicked)
        selected = event.properties.get_piece(state, 0)

        if selected == clicked:
            return False, None, None

        elif selected and self.move_valid(state, selected, event.clicked):

            state = self.move_piece(state, selected, event.clicked)\
                .push_action(MoveAction(selected, event.clicked))
            return True, state, DisplayProperties()

        elif clicked and self.moveable(state, clicked):
            return True, None, DisplayProperties([event.clicked])

        return False, None, None

    def actions(self, state):

        return [MoveAction(piece, pos)
            for piece in state.piece_list()
            if not any(self.types) or piece.type in self.types
            for pos in state.game.SHAPE.positions()
            if self.move_valid(state, piece, pos)]

    def texture(self, state, event, pos):

        if self.hints and event.active:

            selected = event.properties.get_piece(state, 0)

            if selected and self.move_valid(state, selected, pos):

                if state.enemy(pos): return self.icon
                else: return [t.set_opacity(0.2) for t in
                    selected.type.texture(selected, state)]

        return []

    def move_valid(self, state, piece, pos):

        kernel = PathKernel(state.game.SHAPE, piece.pos, pos)

        return state.game.SHAPE.in_bounds(pos) and\
            (not any(self.types) or any(piece.type.ID == t.ID
                for t in self.types)) and\
            pos != piece.pos and\
            (self.stage in [-1, state.turn.stage]) and\
            (self.capture_self or not state.friendly(pos)) and\
            (self.capture_enemy or not state.enemy(pos)) and\
            (self.allow_jumps or kernel.open(state, piece.pos)) and \
            (self.move_enemy or piece.owner_id in
                [state.turn.current_id, -1]) and\
            piece.type.move_valid(state, piece, pos)

    def move_piece(self, state, piece, pos):

        return piece.type.move_piece(state, piece, pos)

    def moveable(self, state, piece):

        return any(self.move_valid(state, piece, pos)
            for pos in state.game.SHAPE.positions())


class RemoveHandler(Handler):

    EVENTS = [BoardEvent]

    def __init__(self, types=[], hints=True, icon=ATTACK_ICON, stage=-1,
            capture_self=True, capture_enemy=True):

        self.types = types
        self.hints = hints
        self.icon = icon
        self.stage = stage
        self.capture_self = capture_self
        self.capture_enemy = capture_enemy

    def apply(self, state, event):

        piece = state.piece(event.clicked)

        if piece and self.remove_valid(state, piece):

            state = self.remove_piece(state, piece)\
                .push_action(RemoveAction(piece))
            return True, state, DisplayProperties()

        return False, None, DisplayProperties()

    def actions(self, state):

        return [RemoveAction(piece)
            for piece in state.piece_list()
            if piece.type in self.types
            if self.remove_valid(state, piece)]

    def texture(self, state, event, pos):

        if self.hints and event.active:

            piece = state.piece(pos)

            if piece and self.remove_valid(state, piece):
                return self.icon

        return []

    def remove_valid(self, state, piece):

        return (not any(self.types) or any(piece.type.ID == t.ID
                for t in self.types)) and\
            (self.stage in [-1, state.turn.stage]) and\
            (self.capture_self or piece.ownerId != state.turn.current) and\
            (self.capture_enemy or piece.ownerId == state.turn.current) and\
            piece.type.remove_valid(state, piece)

    def remove_piece(self, state, piece):

        return piece.type.remove_piece(state, piece)


class SelectHandler(Handler):

    EVENTS = [SelectEvent, BoardEvent]

    def __init__(self, hide=False, hints=False, icon=PLACE_ICON, stage=-1):

        self.hide = hide
        self.hints = hints
        self.icon = icon
        self.stage = stage

    def apply(self, state, event):

        pos = event.clicked if isinstance(event, BoardEvent) else event.target
        enabled = self.enabled(state, pos) and\
            (self.stage in [-1, state.turn.stage])
        options = self.options(state, pos) if enabled else []

        if isinstance(event, BoardEvent) and self.hide and enabled:

            if event.properties.is_selected(pos):
                return True, None, DisplayProperties()

            elif enabled:
                return True, None, DisplayProperties([pos])

        elif isinstance(event, SelectEvent) and enabled and\
                0 <= event.option_id < len(options):

            state = self.select(state, options[event.option_id], pos)\
                .push_action(SelectAction(event.option_id, pos))

            return True, state, DisplayProperties()

        return False, None, None

    def actions(self, state):

        return [SelectAction(option.id, pos)
            for pos in state.game.SHAPE.positions()
            if self.enabled(state, pos)
            for option in self.options(state, pos)]

    def render(self, state, event, display):

        if not event.active: return display

        selectors = [self.selector(state, self.options(state, pos), pos)
            for pos in state.game.SHAPE.positions()
            if self.visible(state, event, pos)]

        return display.add_selectors(selectors)

    def texture(self, state, event, pos):

        if self.hints and event.active and self.enabled(state, pos) and\
                self.stage in [-1, state.turn.stage] and\
                not self.visible(state, event, pos):
            return self.icon

        return []

    def visible(self, state, event, target):

        return self.enabled(state, target) and\
            any(self.options(state, target)) and\
            (not self.hide or event.properties.is_selected(target)) and\
            self.stage in [-1, state.turn.stage]

    def enabled(self, state, target):
        return any(self.options(state, target))

    def options(self, state, target):
        return []

    def selector(self, state, options, target):
        return Selector(options, target, state)

    def select(self, state, option, target):
        return state


class MultiPlaceHandler(SelectHandler, PlaceHandler):

    def __init__(self, types=[], hints=True, icon=PLACE_ICON, stage=-1,
            capture_self=True, capture_enemy=True, hide=True):

        SelectHandler.__init__(self, hide, hints, icon, stage)

        PlaceHandler.__init__(self, None, False, icon, stage,
            capture_self, capture_enemy)

        self.types = types

    def actions(self, state):

        pieces = [Piece(type, state.turn.current_id, pos)
            for pos in state.game.SHAPE.positions()
            if self.enabled(state, pos)
            for type in self.pieces(state, pos)]

        return [PlaceAction(piece) for piece in pieces
            if self.place_valid(state, piece)]

    def options(self, state, target):

        pieces = [Piece(type, state.turn.current_id, target)
            for type in self.pieces(state, target)]

        return [Option(i, piece.type.ID, piece.type.texture(piece, state))
            for i, piece in enumerate(pieces)]

    def pieces(self, state, target):

        pieces = [Piece(type, state.turn.current_id, target)
            for type in self.types]

        return [piece.type for piece in pieces
            if self.place_valid(state, piece)]

    def select(self, state, option, target):

        piece = Piece(state.game.PIECES[option.value],
            state.turn.current_id, target)

        return state.place_piece(piece)\
            .push_action(PlaceAction(piece))
