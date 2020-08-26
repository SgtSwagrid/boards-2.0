from .common.game import *


class HexPiece(PieceType):

    ID = 0
    COLOURS = ['#E55039', '#4A69BD']


class Hex(Game):

    ID = 17
    NAME = 'Hex'
    BACKGROUND = HexCheckerboard(['#ffffff', '#f1f2f6', '#dfe4ea'])
    SHAPE = Star(4)
    PLAYER_NAMES = ['Red', 'Blue']
    INFO = 'https://en.wikipedia.org/wiki/Hex_%28board_game%29'

    PIECES = [HexPiece()]
    HANDLERS = [PlaceHandler(HexPiece(), hints=False)]
