import copy

class BoardEvent:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Display:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.tiles = [[Tile(x, y)
            for y in range(0, height)]
            for x in range(0, width)]

        self.current = False
        self.selections = []

    def set_colours(self, colours):
        display = copy.deepcopy(self)
        for x in range(0, self.width):
            for y in range(0, self.height):
                display.tiles[x][y].colour = colours[x][y]
        return display

    def add_textures(self, textures):
        display = copy.deepcopy(self)
        for x in range(0, self.width):
            for y in range(0, self.height):
                display.tiles[x][y].textures =\
                    display.tiles[x][y].textures + textures[x][y]
        return display

    def set_widths(self, widths):
        display = copy.deepcopy(self)
        for x in range(0, self.width):
            for y in range(0, self.height):
                display.tiles[x][y].width = widths[x]
        return display

    def set_heights(self, heights):
        display = copy.deepcopy(self)
        for x in range(0, self.width):
            for y in range(0, self.height):
                display.tiles[x][y].height = heights[y]
        return display

    def select(self, x, y):
        display = copy.deepcopy(self)
        display.tiles[x][y].selected = True
        display.selections.append((x, y))
        return display

    def clear_selections(self):
        display = copy.deepcopy(self)
        for x in range(0, self.width):
            for y in range(0, self.height):
                display.tiles[x][y].selected = False
        display.selections = []
        return display

    def set_current(self, current):
        display = copy.deepcopy(self)
        display.current = current
        return display

class Tile:

    def __init__(self, x, y, colour='#FFFFFF', textures=[],
            width=1, height=1, selected=False):
        self.x = x
        self.y = y
        self.colour = colour
        self.textures = textures
        self.width = width
        self.height = height
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
