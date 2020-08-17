import math

from games.games.common.game import PieceType, Game
from games.games.common.shapes import Hexagonal, Rectangle


class Star(Hexagonal):

    def __init__(self, star_size):
        self.total_rows = 4 * star_size + 1
        self.total_cols = 3 * star_size + 1
        self.star_size = star_size

        super().__init__(self.total_cols, self.total_rows)

    def row_size(self, y):

        tri_size = self.total_cols
        upper = self.total_rows - y - 1

        tr1 = y+1 if y < tri_size else 1
        tr2 = upper+1 if upper < tri_size else 1

        return max(tr1, tr2)

    def row_indent(self, y):
        return (self.total_cols / 2 - self.row_size(y) / 2) * math.sqrt(3)


class ChineseCheckers(Game):
    ID = 16
    NAME = 'Chinese Checkers'
    # BACKGROUND = ChompBoard(['#5D4037', '#8D6E63'])
    SHAPE = Star(4)
    PLAYER_NAMES = ['Purple', 'Yellow']
    INFO = 'https://en.wikipedia.org/wiki/Chinese_checkers'


