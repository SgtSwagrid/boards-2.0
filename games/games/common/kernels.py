from .vector import *

class Kernel:

    def __init__(self, shape):
        self.shape = shape

    def positions(self, centre):

        return [v for v in self.apply(centre)
            if self.shape.in_bounds(v)]

    def pieces(self, state, centre):

        return [state.piece_at(v)
            for v in self.positions(centre)
            if state.piece_at(v)]

    def find_pieces(self, state, centre,
            player_id=-1, type=-1, mode=-1, x=-1, y=-1):

        return [piece for piece in self.pieces(state, centre)
            if (type == -1 or piece.type.ID == type.ID) and
            (player_id == -1 or piece.owner_id == player_id) and
            (x == -1 or piece.x == x) and (y == -1 or piece.y == y) and
            (mode == -1 or piece.mode == mode)]

    def filled(self, state, centre):

        return all(state.piece_at(v) for v in self.positions(centre))

    def open(self, state, centre):

        return len(self.pieces(state, centre)) == 0


class BoxKernel(Kernel):

    def __init__(self, shape, r0=0, r1=1):

        super().__init__(shape)
        self.r0 = r0
        self.r1 = r1

    def apply(self, centre):

        return [centre + Vec(x, y)
            for r in range(self.r0, self.r1 + 1)
            for x in range(-r, r + 1)
            for y in range(-r, r + 1)]


class DiamondKernel(Kernel):

    def __init__(self, shape, r0=0, r1=1):

        super().__init__(shape)
        self.r0 = r0
        self.r1 = r1

    def apply(self, centre):

        return [centre + Vec(x, y)
            for r in range(self.r0, self.r1 + 1)
            for x in range(-r, r + 1)
            for y in [r - abs(x), abs(x) - r]]

class RayKernel(Kernel):

    def __init__(self, shape, dir, r0=1, r1=-1):

        super().__init__(shape)
        self.dir = dir
        self.r0 = r0
        self.r1 = r1 if r1 != -1 else max(shape.width, shape.height)

    def apply(self, centre):

        return [centre + Vec(r * self.dir.x, r * self.dir.y)
            for r in range(self.r0, self.r1 + 1)]

    def first(self, state, centre):

        pieces = self.pieces(state, centre)
        return pieces[0] if any(pieces) else None

    def extent(self, state, centre):

        while state.open(centre):
            centre = centre + self.dir

        return centre
