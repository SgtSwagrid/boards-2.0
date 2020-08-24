from .state import *
from .display import *
from .events import *
from .backgrounds import *
from .shapes import *
from .handlers import *
from .kernels import *
from .vector import *


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
            for y in range(0, self.SHAPE.logical_board_height())]
            for x in range(0, self.SHAPE.logical_board_end() + 1)]

        state = State(game=self, num_players=num_players, pieces=pieces)

        for player_id in range(0, num_players):
            score = self.initial_score(num_players, player_id)
            state = state.add_score(player_id, score)

        return state

    def initial_piece(self, num_players, x, y):
        return None

    def initial_score(self, num_players, player_id):
        return 0

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

        display = Display(self.SHAPE)

        positions = [[(self.SHAPE.logical_tile_hoffset(row, tile),
            self.SHAPE.logical_row_voffset(row))
            for tile in range(0, self.SHAPE.row_width(row))]
            for row in range(0, self.SHAPE.height)]

        display = display.set_colours([[self.colour(state, event, x, y)
            for (x, y) in row] for row in positions])

        display = display.set_textures([[self.texture(state, event, x, y)
            for (x, y) in row] for row in positions])

        display = display.set_background(self.BACKGROUND.background)

        for handler in self.HANDLERS:
            display = handler.render(state, event, display)

        return display

    def colour(self, state, event, x, y):

        piece_colour = state.pieces[x][y].type.colour(
            state.pieces[x][y], state)\
            if state.pieces[x][y] else None

        if piece_colour: return piece_colour
        elif event.properties.selected(x, y): return self.SELECTED_COLOUR
        elif state.changed(x, y): return self.MODIFIED_COLOUR
        else: return self.BACKGROUND.colour(x, y)

    def texture(self, state, event, x, y):

        textures = self.BACKGROUND.texture(x, y)
        piece = state.pieces[x][y]
        if piece: textures = textures + piece.type.texture(piece, state)

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
