import copy

class Display:

    def __init__(self, rows):
        self.rows = rows
        self.width = max(r.width for r in rows)
        self.height = sum(r.t_spacing + r.height for r in rows)

    def scale(self, width, height):

        display = copy.deepcopy(self)

        display.width = min(width, height * self.width / self.height)
        display.height = min(height, width * self.height / self.width)

        for row in display.rows:
            row.height *= display.height / self.height
            row.t_spacing *= display.height / self.height

            for tile in row.tiles:
                tile.width *= display.width / row.width
                tile.l_spacing *= display.width / row.width

        return display

    def selections(self):
        return [(tile.x, tile.y) for row in self.rows
            for tile in row.tiles if tile.selected]

class Row:

    def __init__(self, tiles, height=1, t_spacing=0):
        self.tiles = tiles
        self.width = sum(t.l_spacing + t.width for t in tiles)
        self.height = height
        self.t_spacing = t_spacing

class Tile:

    def __init__(self, x, y, colour='#FFFFFF', textures=[],
            width=1, l_spacing=0, selected=False):
        self.x = x
        self.y = y
        self.colour = colour
        self.textures = textures
        self.width = width
        self.l_spacing = l_spacing
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
