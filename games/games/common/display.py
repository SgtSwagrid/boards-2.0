import copy
import math

class Display:

    def __init__(self, rows, hexagonal=False):
        self.rows = rows
        self.width = max(r.width for r in rows)
        self.height = rows[0].offset + rows[0].height
        self.hexagonal = hexagonal
        self.selector = None

    def scale(self, width, height):

        display = copy.deepcopy(self)
        sf = min(width / self.width, height / self.height)

        display.width *= sf
        display.height *= sf

        for row in display.rows:
            row.width *= sf
            row.height *= sf
            row.offset *= sf

            for tile in row.tiles:
                tile.width *= sf
                tile.offset *= sf

        if display.selector:
            display.selector.x *= sf
            display.selector.y *= sf
            display.selector.width *= sf
            display.selector.height *= sf

        return display

    def selections(self):
        return [(tile.x, tile.y) for row in self.rows
            for tile in row.tiles if tile.selected]

    def show_selector(self, selector):
        display = copy.copy(self)
        display.selector = selector
        return display

class Row:

    def __init__(self, tiles, height=1, offset=0):
        self.tiles = tiles
        self.width = tiles[-1].offset + tiles[-1].width
        self.height = height
        self.offset = offset

class Tile:

    def __init__(self, x, y, colour='#FFFFFF', textures=[],
            width=1, offset=0, selected=False):
        self.x = x
        self.y = y
        self.colour = colour
        self.textures = [texture if isinstance(texture, Texture)
            else Texture(texture) for texture in textures]
        self.width = width
        self.offset = offset
        self.selected = selected

class Texture:

    def __init__(self, image, opacity=1.0):
        self.image = image
        self.opacity = opacity

    def set_opacity(self, opacity):
        texture = copy.deepcopy(self)
        texture.opacity = opacity
        return texture

class Selector:

    def __init__(self, options, target_x, target_y, shape,
            size=0.5, offset=0.5, colour='#F5F6FA', opacity=0.9):

        self.options = options

        self.width = len(self.options) * size
        self.height = size

        self.target_x = target_x
        self.target_y = target_y

        target_y = shape.height - target_y - 1

        min_x = 0
        max_x = shape.display_width() - self.width
        tile_width = shape.tile_width(target_x, target_y)
        x = target_x - self.width / 2 + tile_width / 2
        self.x = max(min_x, min(max_x, x))

        min_y = 0
        max_y = shape.display_height() - self.height
        row_height = shape.row_height(target_y)
        row_centre = shape.row_centre(target_y)
        bottom = row_centre < shape.display_height() - row_centre
        if bottom: offset *= -1
        y = target_y - self.height / 2 + row_height / 2 + offset
        self.y = max(min_y, min(max_y, y))

        self.colour = colour
        self.opacity = opacity

class PieceSelector(Selector):

    def __init__(self, pieces, state, target_x, target_y, shape,
            size=0.5, offset=0.5, colour='#F5F6FA', opacity=0.9):

        options = [Option(i, piece.type.ID, type(piece.type).__name__,
            piece.type.texture(piece, state))
            for i, piece in enumerate(pieces)]

        super().__init__(options, target_x, target_y, shape,
            size, offset, colour, opacity)

class Option:

    def __init__(self, id, value, name, textures):
        self.id = id
        self.value = value
        self.name = name
        self.textures = [texture if isinstance(texture, Texture)
            else Texture(texture) for texture in textures]
