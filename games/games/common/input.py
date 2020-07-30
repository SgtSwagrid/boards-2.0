import copy

class ClickInput:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Display:

    def __init__(self, width, height):
        self.tiles = [[Tile(x, y)
            for y in range(0, height)]
            for x in range(0, width)]
        self.selections = []
        self.current = False

    def set_colour(self, x, y, colour):
        display = copy.deepcopy(self)
        display.tiles[x][y].colour = colour
        return display

    def add_texture(self, x, y, texture):
        display = copy.deepcopy(self)
        display.tiles[x][y].textures += [texture]
        return display

    def set_width(self, x, y, width):
        display = copy.deepcopy(self)
        display.tiles[x][y].width = width
        return display

    def set_height(self, x, y, height):
        display = copy.deepcopy(self)
        display.tiles[x][y].height = height
        return display

    def select(self, x, y):
        display = copy.deepcopy(self)
        display.tiles[x][y].selected = True
        display.selections = display.selections + [(x, y)]
        return display

    def clear_selections(self):
        display = copy.deepcopy(self)
        for x, y in display.selections:
            display.tiles[x][y].selected = False
        display.selections = []
        return display

    def set_current(self, current):
        display = copy.deepcopy(self)
        display.current = current
        return display

class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = '#FFFFFF'
        self.textures = []
        self.width = 1
        self.height = 1
        self.selected = False

class Texture:

    def __init__(self, image, opacity=1.0, x=0, y=0, width=100, height=100):
        self.image = image
        self.opacity = opacity
        self.x = x
        self.y = y
        self.width = width
        self.height = height