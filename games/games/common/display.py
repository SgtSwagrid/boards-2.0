import copy

class Display:

    def __init__(self, rows, hexagonal=False):
        self.rows = rows
        self.width = max(r.width for r in rows)
        self.height = rows[0].offset + rows[0].height
        self.hexagonal = hexagonal
        self.selectors = []

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

        for selector in display.selectors:
            selector.x *= sf
            selector.y *= sf
            selector.width *= sf
            selector.height *= sf

        return display

    def selections(self):
        return [(tile.x, tile.y) for row in self.rows
            for tile in row.tiles if tile.selected]

    def add_selectors(self, selectors):
        display = copy.copy(self)
        display.selectors = display.selectors + selectors
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

    def __init__(self, options, target_x, target_y, state,
            size=0.5, offset=0.5, colour='#F5F6FA', opacity=0.85):

        self.options = options

        self.width = len(self.options) * size
        self.height = size

        self.target_x = target_x
        self.target_y = target_y

        shape = state.game.SHAPE
        target_y = shape.height - target_y - 1

        min_x = 0
        max_x = shape.display_width() - self.width
        tile_x = shape.tile_centre(target_x, target_y)
        x = tile_x - self.width / 2
        self.x = max(min_x, min(max_x, x))

        min_y = 0
        max_y = shape.display_height() - self.height
        row_y = shape.row_centre(target_y)
        if 2 * row_y > shape.display_height(): offset *= -1
        y = row_y - self.height / 2 + offset
        self.y = max(min_y, min(max_y, y))

        self.colour = colour
        self.opacity = opacity

class Option:

    def __init__(self, id, value, textures):
        self.id = id
        self.value = value
        self.textures = [texture if isinstance(texture, Texture)
            else Texture(texture) for texture in textures]
