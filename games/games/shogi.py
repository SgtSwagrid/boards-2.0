from .common.game import *
from .common.handlers import MoveHandler
from .common.shapes import Rectangle
from .common.backgrounds import Checkerboard


class ShogiPieceType(PieceType):

    def texture(self, piece, state):
        texture = self.TEXTURES[piece.mode][piece.owner_id]
        if not texture:
            return []
        elif isinstance(texture, Texture):
            return [texture]
        else:
            return [Texture(texture)]


class Shogi(Game):
    ID = 11
    NAME = 'Shogi'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(9, 9)
    # TODO if git problem replace Kanji with unicode
    PLAYER_NAMES = ['Sente 先手', 'Gote 後手']

    class OshoGyokusho(ShogiPieceType):
        # osho means King General; Gyokusho means Jeweled General
        ID = 0
        TEXTURES = [['shogi/osho.png', 'shogi/gyokusho_reverse.png']]

    class HishaRyuo(ShogiPieceType):
        # Hisha means flying chariot; Ryuo means dragon king
        ID = 1
        TEXTURES = [['shogi/hisha.png', 'shogi/hisha_reverse.png']]

    class KakugyoRyuma(ShogiPieceType):
        # Kakugyo means angle mover; Ryuma means dragon horse
        ID = 2
        TEXTURES = [['shogi/kakugyo.png', 'shogi/kakugyo_reverse.png']]

    class Kinsho(ShogiPieceType):
        # Kinsho means gold general
        ID = 3
        TEXTURES = [['shogi/kinsho.png', 'shogi/kinsho_reverse.png']]

    class GinshoNarigin(ShogiPieceType):
        # Ginsho means silver general; Narigin means promoted silver
        ID = 4
        TEXTURES = [['shogi/ginsho.png', 'shogi/ginsho_reverse.png']]

    class KeimaNarikei(ShogiPieceType):
        # Keima means cassia horse; Narikei means promoted cassia
        ID = 5
        TEXTURES = [['shogi/keima.png', 'shogi/keima_reverse.png']]

    class KyoshaNarikyo(ShogiPieceType):
        # Kyosha means incense chariot; Narikyo means promoted incense
        ID = 6
        TEXTURES = [['shogi/kyosha.png', 'shogi/kyosha_reverse.png']]

    class FuhyoTokin(ShogiPieceType):
        # Fuhyo means foot soldier; Tokin means reaches gold
        ID = 7
        TEXTURES = [['shogi/fuhyo.png', 'shogi/fuhyo_reverse.png']]

    PIECES = [OshoGyokusho(), HishaRyuo(), KakugyoRyuma(), Kinsho(), GinshoNarigin(), KeimaNarikei(),
              KyoshaNarikyo(), FuhyoTokin()]
    # TODO drop pieces rule when engine feature
    HANDLERS = [MoveHandler()]

    def piece(self, num_players, x, y):
        if y in (0, 8):
            player_id = 0 if y == 0 else 1

            if x in (0, 8):
                return Piece(self.KyoshaNarikyo(), player_id)
            elif x in (1, 7):
                return Piece(self.KeimaNarikei(), player_id)
            elif x in (2, 6):
                return Piece(self.GinshoNarigin(), player_id)
            elif x in (3, 5):
                return Piece(self.Kinsho(), player_id)
            elif x == 4:
                return Piece(self.OshoGyokusho(), player_id)

        elif y in (1, 7):
            player_id = 0 if y == 1 else 1

            if x == 1:
                return Piece(self.KakugyoRyuma(), 0) if player_id == 0 else Piece(self.HishaRyuo(), 1)
            elif x == 7:
                return Piece(self.HishaRyuo(), 0) if player_id == 0 else Piece(self.KakugyoRyuma(), 1)
            else:
                return None

        elif y == 2:
            return Piece(self.FuhyoTokin(), 0)
        elif y == 6:
            return Piece(self.FuhyoTokin(), 1)

        else:
            return None
