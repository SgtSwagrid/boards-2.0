from .state import *
from .display import *
from .events import *
from .backgrounds import *


class Game:

    ID = -1
    NAME = 'Game'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = None
    MIN_PLAYERS, MAX_PLAYERS = 2, 2
    PLAYER_NAMES = [f'Player {i}' for i in range(1, 16 + 1)]
    INFO = ''

    PIECES = []
    HANDLERS = []

    SELECTED_COLOUR = '#6A89CC'
    MODIFIED_COLOUR = '#74B9FF'

    def on_setup(self, num_players):

        def at(piece, x, y):
            return piece.at(x, y) if piece else None

        pieces = [[at(self.initial_piece(num_players, x, y), x, y)
            for y in range(0, self.SHAPE.height)]
            for x in range(0, self.SHAPE.width)]

        return State(game=self, num_players=num_players, pieces=pieces)

    def initial_piece(self, num_players, x, y):
        return None

    def on_event(self, state, event):

        for handler in self.HANDLERS:
            if any(isinstance(event, e) for e in handler.EVENTS):

                consumed, result, properties = handler.apply(state, event)
                if consumed:
                    if result: return self.on_action(result), properties
                    else: return None, properties

        return None, DisplayProperties()

    def on_action(self, state):
        return state.end_turn()

    def get_actions(self, state):

        actions = []
        for handler in self.HANDLERS:
            actions.extend(handler.actions(state))
        return actions

    def on_render(self, state, event):

        display = Display([self.row(state, event, y)
            for y in range(0, self.SHAPE.height)], self.SHAPE.hexagonal)

        for handler in self.HANDLERS:
            display = handler.render(state, event, display)

        return display

    def row(self, state, event, y):

        tiles = [self.tile(state, event, x, y)
            for x in range(0, self.SHAPE.row_size(y))]
        height = self.SHAPE.row_height(y)
        offset = self.SHAPE.row_offset(y)

        return Row(tiles, height, offset)

    def tile(self, state, event, x, y):

        colour = self.colour(state, event, x, y)
        texture = self.texture(state, event, x, y)
        width = self.SHAPE.tile_width(x, y)
        offset = self.SHAPE.tile_offset(x, y)

        return Tile(x, y, colour, texture, width, offset)

    def colour(self, state, event, x, y):

        piece_colour = state.pieces[x][y].type.colour(
            state.pieces[x][y], state)\
            if state.pieces[x][y] else None

        if piece_colour: return piece_colour
        elif event.properties.selected(x, y): return self.SELECTED_COLOUR
        elif state.changed(x, y): return self.MODIFIED_COLOUR
        else: return self.BACKGROUND.colour(
            x + self.SHAPE.pattern_offset(x, y), y)

    def texture(self, state, event, x, y):

        textures = self.BACKGROUND.texture(
            x + self.SHAPE.pattern_offset(x, y), y)
        piece = state.pieces[x][y]
        if piece: textures.extend(piece.type.texture(piece, state))

        if event.active:
            for handler in self.HANDLERS:
                textures.extend(handler.texture(state, event, x, y))

        return textures


class PieceType:

    TEXTURES = [None] * 16
    COLOURS = [None] * 16

    def texture(self, piece, state):
        texture = self.TEXTURES[piece.owner_id]
        if not texture: return []
        elif isinstance(texture, Texture): return [texture]
        else: return [Texture(texture)]

    def colour(self, piece, state):
        return self.COLOURS[piece.owner_id]

    def place_valid(self, state, piece):
        return True

    def place_piece(self, state, piece):
        return state.place_piece(piece)

    def move_valid(self, state, piece, x_to, y_to):
        return True

    def move_piece(self, state, piece, x_to, y_to):
        return state.move_piece(piece, x_to, y_to)

    def remove_valid(self, state, piece):
        return True

    def remove_piece(self, state, piece):
        return state.remove_piece(piece)
