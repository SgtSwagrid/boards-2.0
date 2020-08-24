from .common.game import *


class EdgePiece(PieceType):

    ID = 0
    COLOURS = ['#E74C3C', '#3498DB']

    def place_valid(self, state, piece):

        return ((piece.pos.x % 2 == 0) ^ (piece.pos.y % 2 == 0)) and\
            state.game.SHAPE.in_bounds(piece.pos) and\
            not state.piece_at(piece.pos)

    def place_piece(self, state, piece):

        player_score = state.player_states[state.turn.current_id].score
        state = state.place_piece(piece)
        state = state.game.capture(state, piece)
        player_score_after = state.player_states[state.turn.current_id].score

        return state.end_turn() if player_score == player_score_after else state


class CapturePiece(PieceType):

    ID = 1
    COLOURS = ['#FAB1A0', '#74B9FF']


class DotsAndBoxes(Game):

    ID = 7
    NAME = 'Dots and Boxes'
    BACKGROUND = Gingham(['#FDCB6E', '#2F3640', '#FFEAA7'])
    SHAPE = Table(6, 6, cell_width=5, cell_height=5)
    PLAYER_NAMES = ['Red', 'Blue']
    INFO = 'https://en.wikipedia.org/wiki/Dots_and_Boxes'

    PIECES = [EdgePiece(), CapturePiece()]
    HANDLERS = [PlaceHandler(EdgePiece(), hints=False)]

    def on_action(self, state):

        game_finished = all([state.pieces_at(pos)
            for pos in self.SHAPE.positions()
            if (pos.x % 2 == 1 and pos.y % 2 == 1)])

        return state if not game_finished else state.end_game()

    def capture(self, state, piece):

        adj = self.adjacent_tiles(state, piece)

        for tile in adj:
            if not state.piece_at(tile) and\
                    all(self.adjacent_edges(state, tile)):
                cap_piece = Piece(CapturePiece(),
                    state.turn.current_id, tile)
                state = state\
                    .place_piece(cap_piece)\
                    .add_score(state.turn.current_id, 1)

        return state

    def adjacent_tiles(self, state, piece):

        return [Vec(piece.pos.x+dx, piece.pos.y+dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if ((piece.pos.x+dx) % 2 == 1 and ((piece.pos.y+dy) % 2 == 1))
                and not (dx == 0 and dy == 0)
                and state.open(Vec(piece.pos.x+dx, piece.pos.y+dy))]

    def adjacent_edges(self, state, pos):

        return [state.piece_at(pos)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if (((pos.x+dx) % 2 == 0) ^ ((pos.y+dy) % 2 == 0))
                and not (dx == 0 and dy == 0)]
