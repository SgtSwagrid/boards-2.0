from .common.game import *


class Pawn(PieceType):

    ID = 0
    TEXTURES = ['chess/white_pawn.png', 'chess/black_pawn.png']

    def move_valid(self, state, piece, pos):

        dir = [1, -1][piece.owner_id]
        home = piece.pos.y == [1, 6][piece.owner_id]

        straight = pos.x == piece.pos.x and not state.piece(pos)
        normal = straight and pos.y - piece.pos.y == dir
        double = straight and pos.y - piece.pos.y == 2 * dir and home

        capture = abs(pos.x - piece.pos.x) == 1 and\
            pos.y - piece.pos.y == dir and state.enemy(pos)

        return normal or double or capture or\
            self.en_passant(state, piece, pos)

    def move_piece(self, state, piece, pos):

        if en_passant := self.en_passant(state, piece, pos):
            return en_passant

        else: return state.move_piece(piece, pos)

    def en_passant(self, state, piece, pos):

        capture = abs(pos.x - piece.pos.x) == 1 and\
            pos.y - piece.pos.y == [1, -1][piece.owner_id]

        double = isinstance(state.action, MoveAction) and\
            isinstance(state.action.piece.type, Pawn) and\
            abs(state.action.new_pos.y - state.action.old_pos.y) == 2

        if capture and double:
            direction = (0, [1, -1][state.action.piece.owner_id])

            if pos == state.action.old_pos + direction:
                return state.move_piece(piece, pos)\
                    .remove_piece(state.action.piece)


class Rook(PieceType):

    ID = 1
    TEXTURES = ['chess/white_rook.png', 'chess/black_rook.png']

    def move_valid(self, state, piece, pos):
        return piece.pos.orthogonal(pos)


class Knight(PieceType):

    ID = 2
    TEXTURES = ['chess/white_knight.png', 'chess/black_knight.png']

    def move_valid(self, state, piece, pos):
        d = (pos - piece.pos).abs()
        return (d.x == 1 and d.y == 2) or (d.x == 2 and d.y == 1)


class Bishop(PieceType):

    ID = 3
    TEXTURES = ['chess/white_bishop.png', 'chess/black_bishop.png']

    def move_valid(self, state, piece, pos):
        return piece.pos.diagonal(pos)


class Queen(PieceType):

    ID = 4
    TEXTURES = ['chess/white_queen.png', 'chess/black_queen.png']

    def move_valid(self, state, piece, pos):
        return piece.pos.straight(pos)


class King(PieceType):

    ID = 5
    TEXTURES = ['chess/white_king.png', 'chess/black_king.png']

    def move_valid(self, state, piece, pos):
        return piece.pos.diag_adjacent(pos) or self.castle(state, piece, pos)

    def move_piece(self, state, piece, pos):

        if castle := self.castle(state, piece, pos):
            return castle

        else: return state.move_piece(piece, pos)

    def castle(self, state, king, pos):

        if pos - king.pos in [(-2, 0), (2, 0)] and king.mode == 0:

            dir = king.pos.direction(pos)
            file = {-2: 0, 2: 7}[pos.x - king.pos.x]
            rook = state.piece(Vec(file, king.pos.y))

            if rook and rook.mode == 0:

                path = PathKernel(state.game.SHAPE,
                    king.pos, rook.pos).open(state, king.pos)

                kernel = RayKernel(state.game.SHAPE, dir, 2, 0)
                check = any(state.game.attacking(state, state.turn.next_id, pos)
                    for pos in kernel.positions(king.pos))

                if path and not check:
                    return state.move_piece(king, pos)\
                        .move_piece(rook, king.pos + dir)


class ChessMoveHandler(MoveHandler):

    def move_valid(self, state, piece, pos):

        return super().move_valid(state, piece, pos) and\
            not state.game.check(self.move_piece(state, piece, pos)) and\
            not PromotionHandler().promotion(state)

    def move_piece(self, state, piece, pos):

        state = super().move_piece(state, piece, pos)
        return state.set_piece_mode(state.piece(pos), 1)


class PromotionHandler(MultiPlaceHandler):

    def enabled(self, state, pos):

        return state.friendly(pos) and\
            isinstance(state.piece(pos).type, Pawn) and\
            pos.y == [7, 0][state.turn.current_id]

    def pieces(self, state, pos):

        return [Rook(), Knight(), Bishop(), Queen()]

    def promotion(self, state):

        player_id = state.turn.current_id
        pieces = state.find_pieces(player_id, Pawn(), y=[7, 0][player_id])
        return pieces[0] if any(pieces) else None


class Chess(Game):

    ID = 2
    NAME = 'Chess'
    BACKGROUND = Checkerboard(['#FDCB6E', '#FFEAA7'])
    SHAPE = Rectangle(8, 8)
    PLAYER_NAMES = ['White', 'Black']
    INFO = 'https://en.wikipedia.org/wiki/Chess'

    PIECES = [Pawn(), Rook(), Knight(), Bishop(), Queen(), King()]
    HANDLERS = [
        ChessMoveHandler(allow_jumps=False),
        PromotionHandler(hide=False)
    ]

    def on_action(self, state):

        if PromotionHandler().promotion(state): return state

        elif self.checkmate(state.end_turn()):
            return state.end_game(state.turn.current_id)

        elif self.stalemate(state.end_turn()):
            return state.end_game()

        else: return state.end_turn()

    def initial_piece(self, num_players, pos):

        if pos.y in (0, 7):
            player_id = 0 if pos.y == 0 else 1

            if pos.x in (0, 7): return Piece(Rook(), player_id)
            elif pos.x in (1, 6): return Piece(Knight(), player_id)
            elif pos.x in (2, 5): return Piece(Bishop(), player_id)
            elif pos.x == 3: return Piece(Queen(), player_id)
            elif pos.x == 4: return Piece(King(), player_id)

        elif pos.y in (1, 6): return Piece(Pawn(), 0 if pos.y == 1 else 1)

    def on_render(self, state, event):

        display = super().on_render(state, event)
        return display.rotate() if event.player_id == 1 else display

    def check(self, state):

        king = state.find_pieces(state.turn.current_id, King())[0]
        return self.attacking(state.end_turn(), state.turn.next_id, king.pos)

    def mate(self, state):
        return not any(self.get_actions(state))

    def checkmate(self, state):
        return self.check(state) and self.mate(state)

    def stalemate(self, state):
        return not self.check(state) and self.mate(state)

    def attacking(self, state, player_id, pos):

        return any(piece.type.move_valid(state, piece, pos) and\
            PathKernel(self.SHAPE, piece.pos, pos).open(state, piece.pos)
            for piece in state.find_pieces(player_id))
