import math


class Vec:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def orthogonal(self, v):

        return (v.x - self.x != 0) ^ (v.y - self.y != 0)

    def diagonal(self, v):

        return abs(v.x - self.x) == abs(v.y - self.y) != 0

    def straight(self, v):

        return self.orthogonal(v) or self.diagonal(v)

    def hex_straight(self, v):

        return self.ortogonal(v) or (v.x - self.x) == -(v.y - self.y)

    def taxicab_dist(self, v):

        return abs(v.x - self.x) + abs(v.y - self.y)

    def kings_dist(self, v):

        return max(abs(v.x - self.x), abs(v.y - self.y))

    def direction(self, v):

        if v.x == self.x and v.y == self.y: return Vec(0, 0)
        gcd = math.gcd(abs(v.x - self.x), abs(v.y - self.y))
        return Vec((v.x - self.x) // gcd, (v.y - self.y) // gcd)

    def steps(self, v):

        d = self.direction(v)
        if d.x == d.y == 0: return 0
        elif d.y == 0: return (v.x - self.x) // d.x
        else: return (v.y - self.y) // d.y

    def orth_adjacent(self, v):

        return self.taxicab_dist(v) == 1

    def diag_adjacent(self, v):

        return self.kings_dist(v) == 1

    def hex_adjacent(self, v):

        return (self.y == v.y and abs(v.x - self.x) == 1) or\
            (v.y - self.y == 1 and v.x in [self.x - 1, self.x]) or\
            (v.y - self.y == -1 and v.x in [self.x, self.x + 1])

    def abs(self):

        return Vec(abs(self.x), abs(self.y))

    def __add__(self, v):
        if isinstance(v, Vec): return Vec(self.x + v.x, self.y + v.y)
        else: return Vec(self.x + v[0], self.y + v[1])

    def __sub__(self, v):
        if isinstance(v, Vec): return Vec(self.x - v.x, self.y - v.y)
        else: return Vec(self.x - v[0], self.y - v[1])

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __mul__(self, s):
        return Vec(self.x * s, self.y * s)

    def __eq__(self, v):
        if isinstance(v, Vec): return (self.x, self.y) == (v.x, v.y)
        else: return (self.x, self.y) == v

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))


def directions():

    return [Vec(1, 0), Vec(1, 1), Vec(0, 1), Vec(-1, 1),
        Vec(-1, 0), Vec(-1, -1), Vec(0, -1), Vec(1, -1)]

def positive_directions():
    
    return [Vec(1, 0), Vec(1, 1), Vec(0, 1), Vec(-1, 1)]

def hex_directions():

    return [Vec(1, 0), Vec(0, 1), Vec(-1, 1),
        Vec(-1, 0), Vec(0, -1), Vec(1, -1)]
