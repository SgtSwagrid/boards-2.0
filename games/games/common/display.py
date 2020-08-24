import copy


class Display:

    def __init__(self, shape):

        self.shape = shape

        self.width = shape.visual_board_width()
        self.height = shape.visual_board_height()

        self.background = '#FFFFFF'

        self.rows = [Row(shape, row_id)
            for row_id in range(0, shape.height)]

        self.selectors = []

    def set_colours(self, colours):

        display = copy.deepcopy(self)
        for row, row_colours in zip(display.rows, colours):
            for tile, colour in zip(row.tiles, row_colours):
                tile.colour = colour
        return display

    def set_textures(self, textures):

        display = copy.deepcopy(self)
        for row, row_textures in zip(display.rows, textures):
            for tile, texture in zip(row.tiles, row_textures):
                tile.texture = [t if isinstance(t, Texture)
                    else Texture(t) for t in texture]
        return display

    def set_background(self, colour):

        display = copy.copy(self)
        display.background = colour
        return display

    def add_selectors(self, selectors):

        display = copy.copy(self)
        display.selectors = display.selectors + selectors
        return display

    def scale(self, width, height):

        sf = min(width / self.width, height / self.height)
        display = copy.copy(self)
        display.width *= sf
        display.height *= sf
        display.rows = [row.scale(sf) for row in display.rows]
        display.selectors = [selector.scale(sf)
            for selector in display.selectors]
        return display


class Row:

    def __init__(self, shape, row_id):

        self.shape = shape
        self.row_id = row_id

        self.height = shape.visual_row_height(row_id)
        self.voffset = shape.visual_row_voffset(row_id)

        self.y = shape.logical_row_voffset(row_id)

        self.tiles = [Tile(shape, row_id, tile_id)
            for tile_id in range(0, shape.row_width(row_id))]

    def scale(self, sf):

        row = copy.copy(self)
        row.height *= sf
        row.voffset *= sf
        row.tiles = [tile.scale(sf) for tile in row.tiles]
        return row


class Tile:

    def __init__(self, shape, row_id, tile_id):

        self.shape = shape
        self.row_id = row_id
        self.tile_id = tile_id

        self.colour = '#FFFFFF'
        self.texture = []

        self.width = shape.visual_tile_width(row_id, tile_id)
        self.hoffset = shape.visual_tile_hoffset(row_id, tile_id) -\
            shape.visual_board_start()

        self.x = shape.logical_tile_hoffset(row_id, tile_id) -\
            shape.logical_board_start()

    def scale(self, sf):

        tile = copy.copy(self)
        tile.width *= sf
        tile.hoffset *= sf
        return tile


class Texture:

    def __init__(self, image, opacity=1.0):

        self.image = image
        self.opacity = opacity

    def set_opacity(self, opacity):

        texture = copy.deepcopy(self)
        texture.opacity = opacity
        return texture


class Selector:

    def __init__(self, options, target, state,
            size=0.5, offset=0.5, colour='#F5F6FA', opacity=0.8):

        self.options = options

        self.width = len(self.options) * size
        self.height = size

        self.target = target
        shape = state.game.SHAPE

        row = shape.row(target.y)
        tile = shape.tile(target)

        min_x = 0
        max_x = shape.visual_board_width() - self.width
        tile_x = shape.visual_tile_hcentre(row, tile)
        x = tile_x - self.width / 2
        self.x = max(min_x, min(max_x, x))

        min_y = 0
        max_y = shape.visual_board_height() - self.height
        row_y = shape.visual_row_vcentre(row)
        if row_y > shape.visual_board_height() / 2: offset *= -1
        y = row_y - self.height / 2 + offset
        self.y = max(min_y, min(max_y, y))

        self.colour = colour
        self.opacity = opacity

    def scale(self, sf):

        selector = copy.copy(self)
        selector.width *= sf
        selector.height *= sf
        selector.x *= sf
        selector.y *= sf
        return selector


class Option:

    def __init__(self, id, value, textures):

        self.id = id
        self.value = value
        self.textures = [texture if isinstance(texture, Texture)
            else Texture(texture) for texture in textures]
