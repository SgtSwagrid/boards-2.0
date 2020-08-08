from games.games.common.display import *
from games.games.common.event import *
from games.games.common.state import *


class Game:

    ID = -1
    NAME = f'Game {ID}'
    SIZE = (-1, -1)
    PLAYERS = (2, 2)
    PLAYER_NAMES = [f'Player {i}' for i in range(1, 16 + 1)]

    PIECES = []
    HANDLERS = []

    def in_bounds(self, x, y):
        return 0 <= y < self.height() and 0 <= x < self.width(y)

    def place_valid(self, state, piece):

        return piece and self.in_bounds(piece.x, piece.y) and\
            piece.owner_id == state.turn.current_id and\
            not state.pieces[piece.x][piece.y] and\
            piece.type.place_valid(state, piece)

    def place_piece(self, state, piece):
        return piece.type.place_piece(state, piece)

    def move_valid(self, state, piece, x_to, y_to):

        return piece and self.in_bounds(piece.x, piece.y) and \
            self.in_bounds(x_to, y_to) and \
            piece.owner_id == state.turn.current_id and\
            (x_to != piece.x or y_to != piece.y) and\
            not state.friendly(x_to, y_to) and\
            piece.type.move_valid(state, piece, x_to, y_to)

    def move_piece(self, state, piece, x_to, y_to):
        return piece.type.move_piece(state, piece, x_to, y_to)

    def remove_valid(self, state, piece):
        return piece and self.in_bounds(piece.x, piece.y) and\
            piece.type.remove_valid(state, piece)

    def remove_piece(self, state, piece):
        return piece.type.remove_piece(state, piece)

    def moveable(self, state, piece):
        return piece and piece.owner_id == state.turn.current_id and\
               piece.type.moveable(state, piece)

    def setup(self, num_players):

        pieces = [[self.piece(num_players, x, y)
            for y in range(0, self.height())]
                for x in range(0, self.max_width())]

        return State(game=self, num_players=num_players, pieces=pieces)

    def piece(self, num_players, x, y):
        return None

    def event(self, state, event):

        for handler in self.HANDLERS:
            if isinstance(event, handler.event):

                consumed, result, properties = handler.apply(state, event)
                if consumed: return result, properties

        return None, DisplayProperties()

    def outcome(self, state):
        return state.outcome

    def render(self, state, event):

        return Display([Row([self.tile(state, event, x, y)
            for x in range(0, self.width(y))],
                self.tile_height(y), self.t_spacing(y))
            for y in range(self.height() - 1, -1, -1)])

    def tile(self, state, event, x, y):

        colour = self.colour(state, event, x, y)
        texture = self.texture(state, event, x, y)
        width = self.tile_width(x, y)
        l_spacing = self.l_spacing(x, y)

        return Tile(x, y, colour, texture, width, l_spacing)

    def colour(self, state, event, x, y):

        piece_colour = state.pieces[x][y].type.colour(
            state.pieces[x][y], state)\
            if state.pieces[x][y] else None

        if piece_colour: return piece_colour
        elif event.properties.selected(x, y): return self.SELECTED_COLOUR
        elif state.changed(x, y): return self.MODIFIED_COLOUR
        else: return self.background_colour(x, y)

    def texture(self, state, event, x, y):

        textures = self.background_texture(x, y)
        piece = state.pieces[x][y]
        if piece: textures.extend(piece.type.texture(piece, state))

        if event.active:
            for handler in self.HANDLERS:
                textures.extend(handler.texture(state, event, x, y))

        return textures

    def background_colour(self, x, y):
        return self.checkerboard('#FDCB6E', '#FFEAA7', x, y)

    def background_texture(self, x, y):
        return []

    def checkerboard(self, colour1, colour2, x, y):
        return colour1 if (x + y) % 2 == 0 else colour2

    def table(self, colour1, colour2, x, y):
        return colour1 if x % 2 == 1 and y % 2 == 1 else colour2

    def gingham(self, colour1, colour2, colour3, x, y):
        if (x % 2 == 0) ^ (y % 2 == 0): return colour1
        elif x % 2 == 0 and y % 2 == 0: return colour2
        else: return colour3

    def width(self, y): return self.SIZE[0]
    def height(self): return self.SIZE[1]

    def max_width(self):
        return max(self.width(y) for y in range(0, self.height()))

    def tile_width(self, x, y): return 1
    def tile_height(self, y): return 1
    def l_spacing(self, x, y): return 0
    def t_spacing(self, y): return 0

    SELECTED_COLOUR = '#6A89CC'
    MODIFIED_COLOUR = '#74B9FF'

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
        return False

    def place_piece(self, state, piece):
        return state.place_piece(piece).end_turn()

    def move_valid(self, state, piece, x_to, y_to):
        return False

    def move_piece(self, state, piece, x_to, y_to):
        return state.move_piece(piece, x_to, y_to).end_turn()

    def remove_valid(self, state, piece):
        return False

    def remove_piece(self, state, piece):
        return state.remove_piece(piece).end_turn()

    def moveable(self, state, piece):
        return True