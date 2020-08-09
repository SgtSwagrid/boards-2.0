import copy

class Display:

    def __init__(self, rows, hexagonal=False):
        self.rows = rows
        self.width = max(r.width for r in rows)
        self.height = rows[0].offset + rows[0].height
        self.hexagonal = hexagonal

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

        return display

    def selections(self):
        return [(tile.x, tile.y) for row in self.rows
            for tile in row.tiles if tile.selected]

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

    def __init__(self, image, opacity=1.0, x=0, y=0, width=100, height=100):
        self.image = image
        self.opacity = opacity
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def set_opacity(self, opacity):
        texture = copy.deepcopy(self)
        texture.opacity = opacity
        return texture
