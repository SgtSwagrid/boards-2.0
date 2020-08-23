import math


class Shape:

    def __init__(self, width, height, hexagonal=False):

        self.width = width
        self.height = height
        self.hexagonal = hexagonal

    def row_width(self, row):
        return self.width

    def logical_board_start(self):

        return min(self.logical_row_start(row)
            for row in range(0, self.height))

    def logical_board_end(self):

        return max(self.logical_row_end(row)
            for row in range(0, self.height))

    def logical_board_width(self):

        return self.logical_board_start() - self.logical_board_end() + 1

    def logical_board_height(self):

        return sum(self.logical_row_vspace(y) + 1
            for y in range(0, self.height))

    def logical_row_vspace(self, row):
        return 0

    def logical_row_voffset(self, row):

        return sum(self.logical_row_vspace(y)
            for y in range(0, row + 1)) + row

    def logical_row_start(self, row):

        max_width = max(self.logical_row_width(y)
            for y in range(0, self.height))
        return (max_width - self.logical_row_width(row)) // 2

    def logical_row_end(self, row):

        return self.logical_row_start(row) + self.logical_row_width(row)

    def logical_row_width(self, row):

        return sum(self.logical_tile_hspace(row, x) + 1
            for x in range(0, self.row_width(row)))

    def logical_tile_hspace(self, row, tile):
        return 0

    def logical_tile_hoffset(self, row, tile):

        return sum(self.logical_tile_hspace(row, x)
            for x in range(0, tile + 1)) + tile +\
            self.logical_row_start(row)

    def visual_board_start(self):

        return min(self.visual_row_start(row)
            for row in range(0, self.height))

    def visual_board_end(self):

        return max(self.visual_row_end(row)
            for row in range(0, self.height))

    def visual_board_width(self):

        return self.visual_board_end() - self.visual_board_start()

    def visual_board_height(self):

        return sum(self.visual_row_vspace(y) + self.visual_row_height(y)
            for y in range(0, self.height))

    def visual_row_height(self, row):
        return 1

    def visual_row_vspace(self, row):

        return self.logical_row_vspace(row)

    def visual_row_voffset(self, row):

        return sum(self.visual_row_vspace(y) + self.visual_row_height(y)
            for y in range(0, row)) + self.visual_row_vspace(row)

    def visual_row_vcentre(self, row):

        return self.visual_row_voffset(row) + self.visual_row_height(row) / 2

    def visual_row_start(self, row):

        max_width = max(self.visual_row_width(y)
            for y in range(0, self.height))
        return (max_width - self.visual_row_width(row)) // 2

    def visual_row_end(self, row):

        return self.visual_row_start(row) + self.visual_row_width(row)

    def visual_row_width(self, row):

        return sum(self.visual_tile_hspace(row, x) +
            self.visual_tile_width(row, x)
            for x in range(0, self.row_width(row)))

    def visual_tile_width(self, row, tile):
        return 1

    def visual_tile_hspace(self, row, tile):

        return self.logical_tile_hspace(row, tile)

    def visual_tile_hoffset(self, row, tile):

        return sum(self.visual_tile_hspace(row, x) + self.visual_tile_width(row, x)
            for x in range(0, tile)) + self.visual_tile_hspace(row, tile) +\
            self.visual_row_start(row)

    def visual_tile_hcentre(self, row, tile):

        return self.visual_tile_hoffset(row, tile) +\
            self.visual_tile_width(row, tile) / 2

    def positions(self):

        return [(self.logical_tile_hoffset(row, tile),
            self.logical_row_voffset(row))
            for row in range(0, self.height)
            for tile in range(0, self.row_width(row))]

    def row(self, y):

        row = [row for row in range(0, self.height)
            if self.logical_row_voffset(row) == y]
        return row[0] if len(row) > 0 else -1

    def tile(self, x, y):

        row = self.row(y)
        if row == -1: return -1
        tile = [tile for tile in range(0, self.row_width(row))
            if self.logical_tile_hoffset(row, tile) == x]
        return tile[0] if len(tile) > 0 else -1

    def in_bounds(self, x, y):

        return self.tile(x, y) != -1

    def box_kernel(self, x, y, width, height):

        tiles = [(x - width // 2 + xx, y - height // 2 + yy)
            for xx in range(0, width)
            for yy in range(0, height)]

        return [tile for tile in tiles if self.in_bounds(*tile)]


class Rectangle(Shape):
    pass


class Table(Shape):

    def __init__(self, width, height, cell_width, cell_height):

        super().__init__(2 * width + 1, 2 * height + 1)
        self.cell_width = cell_width
        self.cell_height = cell_height

    def visual_row_height(self, row):
        return 1 if row % 2 == 0 else self.cell_height

    def visual_tile_width(self, row, tile):
        return 1 if tile % 2 == 0 else self.cell_width


class Sections(Shape):

    def __init__(self, h_sections=[], v_sections=[], border=0.1):

        super().__init__(sum(h_sections), sum(v_sections))
        self.h_sections = h_sections
        self.v_sections = v_sections
        self.border = border

    def visual_row_vspace(self, row):

        return self.border if row > 0 and\
            any(row == sum(self.v_sections[0:y])
            for y in range(0, self.height))\
            else 0

    def visual_tile_hspace(self, row, tile):

        return self.border if tile > 0 and\
            any(tile == sum(self.h_sections[0:x])
            for x in range(0, self.width))\
            else 0


class Rows(Shape):

    def __init__(self, rows):

        super().__init__(max(rows), len(rows))
        self.rows = rows

    def row_width(self, row):

        return self.rows[row]


class Hexagonal(Shape):

    def __init__(self, width, height, slanted=False, flipped=False):

        super().__init__(width, height, hexagonal=True)
        self.slanted = slanted
        self.flipped = flipped

    def visual_board_height(self):
        return super().visual_board_height() + 0.5

    def visual_tile_width(self, row, tile):
        return math.sqrt(3)

    def visual_row_vspace(self, row):
        return 0.5

    def visual_tile_hspace(self, row, tile):

        return self.logical_tile_hspace(row, tile) * math.sqrt(3)

    def visual_row_start(self, row):

        offset = self.logical_row_start(row) * math.sqrt(3)

        if not self.slanted:
            if row % 2 == 0 ^ self.flipped: return offset
            else: return offset + math.sqrt(3) / 2

        elif self.slanted:
            y = (self.height - 1 - row) if self.flipped else row
            return offset + y * math.sqrt(3) / 2


class Hexagon(Hexagonal):

    def __init__(self, size):

        super().__init__(2 * size - 1, 2 * size - 1, slanted=True)
        self.size = size

    def row_width(self, row):

        y = (row if row < self.size else self.height - 1 - row)
        return self.size + y

    def logical_row_start(self, row):

        return self.size - 1 - row if row < self.size - 1 else 0


class Star(Hexagonal):
    pass
