from .vector import *
import copy


class PlayerState:

    def __init__(self, order, score=0, mode=0):
        self.order = order
        self.score = score
        self.mode = mode


class Piece:

    def __init__(self, type, owner_id, pos=None, mode=0):
        self.type = type
        self.owner_id = owner_id
        self.pos = pos
        self.mode = mode

    def at(self, pos):
        piece = copy.deepcopy(self)
        piece.pos = pos
        return piece


class Turn:

    def __init__(self, current_id=0, next_id=1,
            stage=0, ply=0, epoch=0, new=True):
        self.current_id = current_id
        self.next_id = next_id
        self.stage = stage
        self.ply = ply
        self.epoch = epoch
        self.new = new


class Outcome:

    def __init__(self, finished=-1, winner_id=-2, draw=-1):

        if winner_id != -2: self.winner = winner_id
        elif draw: self.winner = -1

        if draw != -1: self.draw = draw
        elif winner_id != -2: self.draw = winner_id == -1
        else: self.draw = False

        if finished != -1: self.finished = finished
        else: self.finished = self.winner != -1 or self.draw


class Change:

    def __init__(self, pos, old, new):
        self.pos = pos
        self.old = old
        self.new = new


class State:

    def __init__(self, game, num_players=0, player_states=None, pieces=None, action=None,
            changes=[], turn=Turn(), outcome=Outcome(), previous=lambda: None):

        self.game = game

        self.num_players = num_players if (num_players > 0)\
            else len(player_states)

        self.player_states = player_states if player_states else\
            [PlayerState(i) for i in range(0, num_players)]

        self.pieces = pieces if pieces else\
            [[None] * game.SHAPE.logical_board_height()] *\
            (game.SHAPE.logical_board_end() + 1)

        self.action = action
        self.changes = changes
        self.turn = turn
        self.outcome = outcome
        self.previous = previous

    def piece(self, pos):

        return self.pieces[pos.x][pos.y]

    def piece_list(self):

        return [piece for col in self.pieces for piece in col if piece]

    def find_pieces(self, player_id=-1, type=-1, mode=-1, x=-1, y=-1):

        return [piece for piece in self.piece_list()
            if (type == -1 or piece.type.ID == type.ID) and
            (player_id == -1 or piece.owner_id == player_id) and
            (x == -1 or piece.pos.x == x) and (y == -1 or piece.pos.y == y) and
            (mode == -1 or piece.mode == mode)]

    def end_stage(self, skip=1):

        state = copy.deepcopy(self)
        state.turn.stage += skip
        return state

    def set_stage(self, stage):

        state = copy.deepcopy(self)
        state.turn.stage = stage
        return state

    def end_turn(self, skip=1):

        state = copy.deepcopy(self)
        state.turn.current_id = (state.turn.current_id + skip)\
            % len(state.player_states)
        state.turn.next_id = (state.turn.current_id + 1)\
            % len(state.player_states)
        state.turn.stage = 0
        state.turn.ply += 1
        state.turn.new = True
        return state

    def end_stage_or_turn(self, stages):

        if self.turn.stage < stages - 1: return self.end_stage()
        else: return self.end_turn()

    def end_epoch(self, skip=1):

        state = copy.deepcopy(self)
        state.turn.epoch += skip
        return state

    def end_game(self, winner_id=-2):

        state = self.end_turn()
        if winner_id == -2: winner_id = self.highest_scorer()
        state.outcome.finished = True
        state.outcome.winner_id = winner_id
        state.outcome.draw = winner_id == -1
        return state

    def set_outcome(self, outcome):

        state = copy.deepcopy(self)
        state.outcome = outcome
        return state

    def set_piece(self, piece, pos):

        state = copy.deepcopy(self)
        state.pieces[pos.x][pos.y] = piece
        change = Change(pos, self.piece(pos), piece)
        return state.set_changed(change)

    def set_piece_mode(self, piece, mode):

        state = copy.deepcopy(self)
        state.pieces[piece.pos.x][piece.pos.y] = copy.deepcopy(piece)
        state.pieces[piece.pos.x][piece.pos.y].mode = mode
        return state

    def place_piece(self, piece):

        return self.set_piece(piece, piece.pos)\
            if piece else self

    def move_piece(self, piece, pos):

        return self.remove_piece(piece)\
            .place_piece(piece.at(pos))

    def remove_piece(self, piece):

        return self.set_piece(None, piece.pos)

    def set_score(self, player_id, score):

        state = copy.deepcopy(self)
        state.player_states[player_id].score = score
        return state

    def add_score(self, player_id, score):

        total = self.player_states[player_id].score + score
        return self.set_score(player_id, total)

    def highest_scorer(self):

        players = sorted(self.player_states, key=lambda p: p.score)
        return players[-1].order if players[-1].score > players[-2].score else -1

    def set_player_mode(self, player_id, mode):

        state = copy.deepcopy(self)
        state.player_states[player_id].mode = mode
        return state

    def exists(self, pos):

        return self.game.SHAPE.in_bounds(pos) and self.piece(pos)

    def open(self, pos):

        return self.game.SHAPE.in_bounds(pos) and not self.piece(pos)

    def friendly(self, pos, player_id=-1):

        if player_id == -1: player_id = self.turn.current_id
        return self.exists(pos) and \
               self.piece(pos).owner_id == player_id

    def enemy(self, pos, player_id=-1):

        if player_id == -1: player_id = self.turn.current_id
        return self.exists(pos) and \
               self.piece(pos).owner_id != player_id

    def push_action(self, action):

        state = copy.deepcopy(self)
        state.action = action
        return state

    def set_changed(self, change):

        state = copy.deepcopy(self)
        if state.turn.new: state.changes = []
        state.changes.append(change)
        state.turn.new = False
        return state

    def changed(self, pos):

        return any(c.pos == pos for c in self.changes)
