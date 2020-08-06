from games.games.common.input import *
from games.games.common.state import *

class Game:

    types = []
    handlers = []
    player_names = [f'Player {i}' for i in range(1, 17)]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def place_valid(self, state, piece):

        return piece and self.in_bounds(piece.x, piece.y) and\
            piece.owner == state.turn.current and\
            not state.pieces[piece.x][piece.y] and\
            piece.type.place_valid(state, piece)

    def place_piece(self, state, piece):
        return piece.type.place_piece(state, piece)

    def move_valid(self, state, piece, x_to, y_to):

        return piece and self.in_bounds(piece.x, piece.y) and \
            self.in_bounds(x_to, y_to) and \
            piece.owner == state.turn.current and\
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
        return piece and piece.owner == state.turn.current and\
               piece.type.moveable(state, piece)

    def positions(self, mapper):
        return [[mapper(x, y)
            for y in range(0, self.height)]
            for x in range(0, self.width)]

    def setup(self):

        pieces = [[self.piece(x, y)
            for y in range(0, self.height)]
                for x in range(0, self.width)]

        return State(game=self, pieces=pieces)

    def piece(self, x, y):
        return None

    def event(self, state, display, event):

        for handler in self.handlers:
            if isinstance(event, handler.event):

                result, display = handler.apply(state, display, event)
                if result:
                    outcome = self.outcome(result)
                    return result.set_outcome(outcome), display

        return None, display

    def outcome(self, state):
        return state.outcome

    def display(self, state, display):

        colours = self.positions(lambda x, y:
            self.colour(state, display, x, y))

        textures = self.positions(lambda x, y:
            self.texture(state, display, x, y))

        widths = [self.h_scale(x) for x in range(0, self.width)]
        heights = [self.v_scale(y) for y in range(0, self.height)]

        display = display.set_colours(colours)\
            .add_textures(textures)\
            .set_widths(widths)\
            .set_heights(heights)

        if display.mode.active:
            for handler in self.handlers:
                display = handler.display(state, display)

        return display

    def colour(self, state, display, x, y):

        piece_colour = state.pieces[x][y].type.colour(
            state.pieces[x][y], state, display)\
            if state.pieces[x][y] else None

        if piece_colour: return piece_colour
        elif display.tiles[x][y].selected: return self.selected_colour
        elif state.changed(x, y): return self.modified_colour
        else: return self.background_colour(x, y)

    def texture(self, state, display, x, y):

        textures = self.background_texture(x, y)
        piece = state.pieces[x][y]
        if piece:
            texture = piece.type.texture(piece, state, display)
            if texture: textures.append(texture)
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

    def h_scale(self, x):
        return 1

    def v_scale(self, y):
        return 1

    attack_icon = Texture('games/img/common/attack.png', 0.8)
    place_icon = Texture('games/img/common/place.png', 0.8)
    selected_colour = '#6A89CC'
    modified_colour = '#74B9FF'

class PieceType:

    def texture(self, piece, state, display):
        return None

    def colour(self, piece, state, display):
        return None

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
