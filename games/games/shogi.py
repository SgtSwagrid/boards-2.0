from .common.state import *
from .common.display import *
from .common.event import *
from .common.shapes import Rectangle
from .common.backgrounds import Checkerboard


class Shogi(Game):

    ID = 11
    NAME = 'Game'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(9, 9)
    MIN_PLAYERS, MAX_PLAYERS = 2, 2
    PLAYER_NAMES = ['Sente 先手', 'Gote 後手']

    PIECES = []
    HANDLERS = []
