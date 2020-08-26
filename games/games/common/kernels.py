from .vector import *


class Kernel:

    def __init__(self, shape):
        self.shape = shape

    def positions(self, centre):

        return [v + centre for v in self.apply()
            if self.shape.in_bounds(v + centre)]

    def pieces(self, state, centre):

        return [state.piece(v)
                for v in self.positions(centre)
                if state.piece(v)]

    def find_pieces(self, state, centre,
            player_id=-1, type=-1, mode=-1, x=-1, y=-1):

        return [piece for piece in self.pieces(state, centre)
            if (type == -1 or piece.type.ID == type.ID) and
            (player_id == -1 or piece.owner_id == player_id) and
            (x == -1 or piece.x == x) and (y == -1 or piece.y == y) and
            (mode == -1 or piece.mode == mode)]

    def filled(self, state, centre):

        return all(state.piece(v) for v in self.positions(centre))

    def open(self, state, centre):

        return not any(self.pieces(state, centre))

    def sweep(self):

        return [self.positions(pos) for pos in self.shape.positions()]


class AreaKernel(Kernel):

    def __init__(self, shape, width, height):

        super().__init__(shape)
        self.width = width
        self.height = height

    def apply(self):

        return [Vec(x, y)
            for x in range(0, self.width)
            for y in range(0, self.height)]


class BoxKernel(Kernel):

    def __init__(self, shape, r1=1, r0=0):

        super().__init__(shape)
        self.r1 = r1
        self.r0 = r0

    def apply(self):

        return [Vec(x, y)
            for r in range(self.r0, self.r1 + 1)
            for x in range(-r, r + 1)
            for y in (range(-r, r + 1) if x in [-r, r] else [-r, r])]


class DiamondKernel(Kernel):

    def __init__(self, shape, r1=1, r0=0):

        super().__init__(shape)
        self.r1 = r1
        self.r0 = r0

    def apply(self):

        return [Vec(x, y)
            for r in range(self.r0, self.r1 + 1)
            for x in range(-r, r + 1)
            for y in [r - abs(x), abs(x) - r]]


class HexKernel(Kernel):

    def __init__(self, shape, r1=1, r0=0):

        super().__init__(shape)
        self.r1 = r1
        self.r0 = r0

    def apply(self):

        return [Vec(x, y)
            for r in range(self.r0, self.r1 + 1)
            for x in range(-r, r + 1)
            for y in ([abs(r - abs(x)) * (-1 if x < 0 else 1),
                r * (1 if x < 0 else -1)] if x not in [-r, r] else
                range(0, r + 1) if x < 0 else range(-r, 1))]


class RayKernel(Kernel):

    def __init__(self, shape, dir, max_dist=-1, min_dist=1):

        super().__init__(shape)
        self.dir = dir
        self.max_dist = max_dist if max_dist != -1 else\
            max(shape.width, shape.height)
        self.min_dist = min_dist

    def apply(self):

        return [Vec(r * self.dir.x, r * self.dir.y)
            for r in range(self.min_dist, self.max_dist + 1)]

    def first(self, state, centre):

        pieces = self.pieces(state, centre)
        return pieces[0] if any(pieces) else None

    def extent(self, state, centre):

        while state.open(centre + self.dir):
            centre = centre + self.dir

        return centre


class PathKernel(RayKernel):

    def __init__(self, shape, start, end, inclusive=False):

        dir = start.direction(end)
        dist = start.steps(end)

        max = dist if inclusive else dist - 1
        min = 0 if inclusive else 1

        super().__init__(shape, dir, max, min)
