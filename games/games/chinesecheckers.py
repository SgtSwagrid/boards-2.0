import math

from games.games.common.game import PieceType, Game
from games.games.common.shapes import Star, Hexagon, StaggeredHexagonal, SlantedHexagonal, Hexagonal







class ChineseCheckers(Game):
    ID = 18
    NAME = 'Chinese Checkers'
    # BACKGROUND = ChompBoard(['#5D4037', '#8D6E63'])
    SHAPE = Star(4)
    PLAYER_NAMES = ['Purple', 'Yellow']
    INFO = 'https://en.wikipedia.org/wiki/Chinese_checkers'


