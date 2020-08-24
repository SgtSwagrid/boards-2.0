from .common.game import *


class Man(PieceType):

    ID = 0
    TEXTURES = ['chess/white_pawn.png', 'chess/black_pawn.png']

    def move_valid(self, state, piece, x_to, y_to):

        dist = chebyshev_distance(piece.x, piece.y, x_to, y_to)
        dir = direction(piece.x, piece.y, x_to, y_to)
        jx, jy = piece.x + dir.x, piece.y + dir.y
        capture = self.can_capture(state, None)
        stage = state.turn.stage

        plain = dist == 1 and not capture and stage == 0
        canter = dist == 2 and state.friendly(jx, jy) and not capture
        jump = dist == 2 and state.enemy(jx, jy)

        return plain or canter or jump

    def can_capture(self, state, pieces):

        if state.turn.stage == 0:
            return any(self.piece_can_capture(state, piece)
                for piece in state.find_piece(state.turn.current_id))

        else: return self.piece_can_capture(state, state.action.piece)

    def piece_can_capture(self, state, piece):

        return any(state.enemy(piece.x + dx, piece.y + dy) and\
            state.open(piece.x + dx, piece.y + dy)
            for dx, dy in directions())

    def move_piece(self, state, piece, x_to, y_to):

        dist = chebyshev_distance(piece.x, piece.y, x_to, y_to)
        dir = direction(piece.x, piece.y, x_to, y_to)

        if dist == 2 and state.enemy(piece.x + dir.x, piece.y + dir.y):
            piece = state.pieces[piece.x + dir.x][piece.y + dir.y]
            state = state.remove_piece(piece)

        return state.move_piece(piece, x_to, y_to)


class Knight(Man):

    ID = 1
    TEXTURES = ['chess/white_knight.png', 'chess/black_knight.png']

    def move_valid(self, state, piece, x_to, y_to):
        pass


class Camelot(Game):

    ID = 15
    NAME = 'Camelot'
    SHAPE = Rows([2, 8, 10] + ([12] * 10) + [10, 8, 2])
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.m.wikipedia.org/wiki/Camelot_(board_game)'

    PIECES = [Man(), Knight()]
    HANDLERS = [MoveHandler(PIECES, capture_enemy=False)]

    def on_action(self, action):
        pass

    def initial_piece(self, num_players, x, y):

        if (y == 5 and 3 <= x <= 8) or (y == 6 and 4 <= x <= 7):
            return Piece(Man(), 0)

        elif (x, y) in [(2, 5), (9, 5), (3, 6), (8, 6)]:
            return Piece(Knight(), 0)

        elif (y == 10 and 3 <= x <= 8) or (y == 9 and 4 <= x <= 7):
            return Piece(Man(), 1)

        elif (x, y) in [(2, 10), (9, 10), (3, 9), (8, 9)]:
            return Piece(Knight(), 1)
