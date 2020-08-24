from .common.game import *


class ChineseCheckers(Game):

    ID = 18
    NAME = 'Chinese Checkers'
    BACKGROUND = HexCheckerboard(['#ffffff', '#f1f2f6', '#dfe4ea'])
    SHAPE = Star(4)
    PLAYER_NAMES = ['Purple', 'Yellow']
    INFO = 'https://en.wikipedia.org/wiki/Chinese_checkers'
