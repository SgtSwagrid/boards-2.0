class Background:

    def __init__(self, colours, background='#273C75'):
        self.colours = colours
        self.background = background

    def colour(self, x, y):
        return '#FFFFFF'

    def texture(self, x, y):
        return []

class Solid(Background):

    def colour(self, x, y):
        return self.colours[0]

class Checkerboard(Background):

    def colour(self, x, y):
        return self.colours[0] if (x + y) % 2 == 0 else self.colours[1]

class Table(Background):

    def colour(self, x, y):
        return self.colours[0] if x % 2 == 1 and y % 2 == 1 else self.colours[1]

class Gingham(Background):

    def colour(self, x, y):
        if (x % 2 == 0) ^ (y % 2 == 0): return self.colours[0]
        elif x % 2 == 0 and y % 2 == 0: return self.colours[1]
        else: return self.colours[2]

class HexCheckerboard(Background):

    def colour(self, x, y):
        if (x + (y % 2)) % 3 == 0: return self.colours[0]
        elif (x + (y % 2)) % 3 == 1: return self.colours[1]
        else: return self.colours[2]
