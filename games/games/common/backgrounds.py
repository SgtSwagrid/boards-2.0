class Background:

    def __init__(self, colours, background='#273C75'):

        self.colours = colours
        self.background = background

    def colour(self, pos):
        return '#FFFFFF'

    def texture(self, pos):
        return []


class Solid(Background):

    def colour(self, pos):

        return self.colours[0]


class Checkerboard(Background):

    def colour(self, pos):

        if (pos.x + pos.y) % 2 == 0:
            return self.colours[0]
        else: return self.colours[1]


class TableOutline(Background):

    def colour(self, pos):

        if pos.x % 2 == 1 and pos.y % 2 == 1:
            return self.colours[0]
        else: return self.colours[1]


class Gingham(Background):

    def colour(self, pos):

        if (pos.x % 2 == 0) ^ (pos.y % 2 == 0): return self.colours[0]
        elif pos.x % 2 == 0 and pos.y % 2 == 0: return self.colours[1]
        else: return self.colours[2]


class HexCheckerboard(Background):

    def colour(self, pos):

        if (2 * pos.x + pos.y) % 3 == 0: return self.colours[0]
        elif (2 * pos.x + pos.y) % 3 == 1: return self.colours[1]
        else: return self.colours[2]
