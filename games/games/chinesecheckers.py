from games.games.common.game import PieceType, Game
from games.games.common.shapes import Hexagonal


class Star(Hexagonal):

    def __init__(self, star_size):
        self.total_rows = 4 * star_size + 1
        self.total_cols = 3 * star_size + 1
        self.star_size = star_size

        super().__init__(self.total_cols, self.total_rows)

    def row_size(self, y):
        if 0 <= y < self.star_size:
            return y+1;
        elif self.total_rows > y >= (self.total_rows - self.star_size):
            return self.total_rows - y
        elif self.star_size <= y <= self.total_rows // 2:
            return self.total_cols + self.star_size - y
        elif self.total_rows // 2 < y <= self.total_rows - self.star_size:
            return self.total_cols + self.star_size - y
        else:
            return self.total_cols

class CheckersPiece(PieceType):
    pass


class ChineseCheckers(Game):
    ID = 16
    NAME = 'Chinese Checkers'
    # BACKGROUND = ChompBoard(['#5D4037', '#8D6E63'])
    SHAPE = Star(4)
    PLAYER_NAMES = ['Purple', 'Yellow']
    INFO = 'https://en.wikipedia.org/wiki/Chinese_Chequers'


