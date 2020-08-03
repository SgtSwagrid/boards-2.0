from games.games.common.input import *
from games.games.common.state import *

import time as timer

class Game:

    types = []
    handlers = []

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

    def event(self, state, display, event):

        for handler in self.handlers:
            if isinstance(event, handler.event):
                result, display = handler.apply(state, display, event)
                if result: return result, display
        return None, display

    def setup(self):

        pieces = [[self.piece(x, y)
            for y in range(0, self.height)]
                for x in range(0, self.width)]

        return State(game=self, pieces=pieces)

    def piece(self, x, y):
        return None

    def display(self, state, display):

        scale_x_sum = 0
        scale_y_sum = 0

        for x in range(0, self.width):
            dx, _ = self.scale(x, 0)
            scale_x_sum += dx

        for y in range(0, self.height):
            _, dy = self.scale(0, y)
            scale_y_sum += dy

        display_width = 800
        tile_width = float(display_width / scale_x_sum)
        tile_height = tile_width

        for x in range(0, self.width):
            for y in range(0, self.height):

                colour = self.colour(state, display, x, y)
                display = display.set_colour(x, y, colour)

                sx, sy = self.scale(x, y)
                display = display \
                    .set_sx(x, y, sx * tile_width) \
                    .set_sy(x, y, sy * tile_height)

                if state.pieces[x][y]:
                    texture = self.texture(state, x, y)
                    display = display.add_texture(x, y, Texture(texture))

        if display.current:
            for handler in self.handlers:
                display = handler.display(state, display)

        return display

    def colour(self, state, display, x, y):
        if display.tiles[x][y].selected: return self.selected_colour
        elif state.changed(x, y): return self.modified_colour
        else: return self.background(x, y)

    def background(self, x, y):
        if (x + y) % 2 == 0: return '#FDCB6E'
        else: return '#FFEAA7'

    attack_icon = Texture('games/img/common/attack.png', 0.8)
    place_icon = Texture('games/img/common/place.png', 0.8)
    selected_colour = '#6A89CC'
    modified_colour = '#74B9FF'

    def texture(self, state, x, y):
        piece = state.pieces[x][y]
        if piece: return piece.type.texture(piece.owner)
        else: return None

    def scale(self, x, y):
        return 1, 1

class PieceType:

    def texture(self, owner):
        return 'games/img/empty.png'

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