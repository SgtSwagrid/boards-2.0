from django.db import models
from django.contrib.auth.models import User
from games.games.common.actions import *
from games.games.common.games import *
from datetime import time
import random

from .games.common.state import *

class BoardManager(models.Manager):

    def create(self, game):

        code = hex(random.randint(0, 1048575))[2:].zfill(5).upper()
        state = game.on_setup(game.MAX_PLAYERS)
        state_model = StateModel.states.create(state, previous=None)
        board = super().create(game_id=game.ID, code=code, state=state_model)
        return board

class BoardModel(models.Model):

    boards = BoardManager()

    game_id = models.IntegerField()

    code = models.CharField(max_length=5)

    state = models.ForeignKey('StateModel',
        on_delete=models.SET_NULL, null=True, blank=True)

    status = models.IntegerField(default=0)

    rematch = models.ForeignKey('BoardModel',
        on_delete=models.SET_NULL, null=True)

    time = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ['-time']

    def __str__(self): return self.code + " " + self.game().NAME

    def set_state(self, state):
        self.state = StateModel.states.create(state, previous=self.state)
        if self.state.outcome != -2: self.status = 2
        self.save()

    def is_current(self, player):
        return player is not None and player.order == self.state.current

    def players(self):
        return PlayerModel.objects.filter(board=self)

    def player(self, user):
        return self.players().filter(user=user).first()\
            if user.is_authenticated else None

    def game(self):
        return games[self.game_id]

    def current(self):
        return self.players()[self.state.current]\
            if self.state.outcome == -2 else None

    def winner(self):
        return self.players()[self.state.outcome]\
            if self.state.outcome > -1 else None

    def join(self, user):
        if len(self.players()) < self.game().MAX_PLAYERS\
                and not any(self.players().filter(user=user)):
            order = self.players().count()
            PlayerModel.objects.create(user=user, board=self,
                order=order, leader=order == 0)

    def start(self):
        self.status = 1
        self.state.delete()
        state = self.game().on_setup(len(self.players()))
        self.state = StateModel.states.create(state, previous=None)
        self.save()

    def join_rematch(self, user):
        if not self.rematch:
            self.rematch = BoardModel.boards.create(self.game())
        self.save()
        self.rematch.join(user)
        return self.rematch

    def first(self):
        first = self.state
        while first.previous:
            first = first.previous
        return first

class PlayerModel(models.Model):

    user = models.ForeignKey(User,
        on_delete=models.SET_NULL, null=True)

    board = models.ForeignKey(BoardModel, on_delete=models.CASCADE)

    order = models.IntegerField()

    score = models.IntegerField(default=0)

    leader = models.BooleanField(default=False)

    time = models.TimeField(default=time(0, 0, 0))

    resigned = models.BooleanField(default=False)

    class Meta: ordering = ['board', 'order']

    def __str__(self): return self.board.code + " " + self.user.username

    def leave(self):

        for player in self.board.players().filter(order__gt=self.order):
            player.order -= 1
            player.save()
        self.delete()

        if self.leader:
            other_player = self.board.players().first()
            if other_player:
                other_player.leader = True
                other_player.save()
            else:
                self.board.delete()

    def promote(self):

        other_player = self.board.players().get(order=self.order-1)
        other_player.order += 1
        other_player.save()
        self.order -= 1
        self.save()

    def demote(self):

        other_player = self.board.players().get(order=self.order+1)
        other_player.order -= 1
        other_player.save()
        self.order += 1
        self.save()

    def transfer(self):

        other_player = self.board.players().get(leader=True)
        other_player.leader = False
        other_player.save()
        self.leader = True
        self.save()

    def resign(self):

        self.resigned = True
        self.save()
        remaining = self.board.players().filter(resigned=False)
        if len(remaining) == 1:
            self.board.state.outcome = remaining.get().order
            self.board.state.save()
            self.board.status = 2
            self.board.save()

class StateManager(models.Manager):

    def create(self, state, previous):

        action = ActionModel.actions.create(state.action)\
            if state.action else None

        state_model = super().create(
            game_id=state.game.ID,
            action=action,
            current=state.turn.current_id,
            stage=state.turn.stage,
            ply=state.turn.ply,
            epoch=state.turn.epoch,
            outcome=-2 if not state.outcome.finished else
                -1 if state.outcome.draw else
                state.outcome.winner_id,
            previous=previous)

        for player_state in state.player_states:
            PlayerStateModel.players.create(player_state, state_model)

        for col in state.pieces:
            for piece in col:
                if piece:
                    PieceModel.pieces.create(piece, state_model)

        for change in state.changes:
            ChangeModel.changes.create(change, state_model)

        return state_model

class StateModel(models.Model):

    states = StateManager()

    game_id = models.IntegerField()

    action = models.ForeignKey('ActionModel',
        on_delete=models.CASCADE, null=True)

    current = models.IntegerField(default=0)

    stage = models.IntegerField(default=0)

    ply = models.IntegerField(default=0)

    epoch = models.IntegerField(default=0)

    outcome = models.IntegerField(default=-2)

    previous = models.ForeignKey('StateModel',
        on_delete=models.CASCADE, null=True)

    def get_player_states(self):

        return [p.get_player() for p in
            PlayerStateModel.players.filter(state=self)]

    def get_piece(self, pos):
        piece = PieceModel.pieces.filter(state=self, x=pos.x, y=pos.y)
        return piece.get().get_piece() if piece.exists() else None

    def get_pieces(self):

        game = games[self.game_id]
        piece_set = PieceModel.pieces.filter(state=self)
        pieces = []

        for x in range(0, game.SHAPE.logical_board_end()):
            col_set = piece_set.filter(x=x)
            col = []

            for y in range(0, game.SHAPE.logical_board_height()):
                piece = col_set.filter(y=y)
                col.append(piece.get().get_piece() if piece.exists() else None)

            pieces.append(col)
        return pieces

    def get_action(self):
        return self.action.get_action(self) if self.action else None

    def get_turn(self):

        return Turn(
            current_id=self.current,
            next_id=(self.current + 1) % len(self.get_player_states()),
            stage=self.stage,
            ply=self.ply,
            epoch=self.epoch,
            new=not self.previous or self.previous.current != self.current)

    def get_outcome(self):

        return Outcome(
            finished=self.outcome > -2,
            winner_id=self.outcome,
            draw=self.outcome == -1)

    def get_changes(self):
        return [c.get_change() for c in ChangeModel.changes.filter(state=self)]

    def get_state(self):

        return State(
            game=games[self.game_id],
            player_states=self.get_player_states(),
            pieces=self.get_pieces(),
            action=self.get_action(),
            changes=self.get_changes(),
            turn=self.get_turn(),
            outcome=self.get_outcome(),
            previous=self.get_previous_state)

    def get_previous_state(self):
        return self.previous.get_state() if self.previous else None

class PlayerStateManager(models.Manager):

    def create(self, player, state):

        return super().create(
            state=state,
            order=player.order,
            score=player.score,
            mode=player.mode)

class PlayerStateModel(models.Model):

    players = PlayerStateManager()

    state = models.ForeignKey(StateModel, on_delete=models.CASCADE)

    order = models.IntegerField()

    score = models.IntegerField(default=0)

    mode = models.IntegerField(default=0)

    class Meta: ordering = ['state', 'order']

    def get_player(self):

        return PlayerState(
            order=self.order,
            score=self.score,
            mode=self.mode)

class PieceManager(models.Manager):

    def create(self, piece, state):

        return super().create(
            state=state,
            type=piece.type.ID,
            owner=piece.owner_id,
            x=piece.pos.x,
            y=piece.pos.y,
            mode=piece.mode)

class PieceModel(models.Model):

    pieces = PieceManager()

    state = models.ForeignKey(StateModel, on_delete=models.CASCADE)

    type = models.IntegerField()

    owner = models.IntegerField()

    x = models.IntegerField()

    y = models.IntegerField()

    mode = models.IntegerField(default=0)

    class Meta: ordering = ['state']

    def get_piece(self):

        return Piece(
            type=games[self.state.game_id].PIECES[self.type],
            owner_id=self.owner,
            pos=Vec(self.x, self.y),
            mode=self.mode)

class ActionManager(models.Manager):

    def create(self, action):

        if isinstance(action, PlaceAction):
            action_model = super().create(type=0,
                x_to=action.new_pos.x,
                y_to=action.new_pos.y)

        elif isinstance(action, MoveAction):
            action_model = super().create(type=1,
                x_from=action.old_pos.x,
                y_from=action.old_pos.y,
                x_to=action.new_pos.x,
                y_to=action.new_pos.y)

        elif isinstance(action, RemoveAction):
            action_model = super().create(type=2,
                x_from=action.old_pos.x,
                y_from=action.old_pos.y)

        elif isinstance(action, SelectAction):
            action_model = super().create(type=3,
                option=action.option_id,
                x_to=action.target.x,
                y_to=action.target.y)

        return action_model

class ActionModel(models.Model):

    actions = ActionManager()

    type = models.IntegerField()

    x_from = models.IntegerField(default=-1)

    y_from = models.IntegerField(default=-1)

    x_to = models.IntegerField(default=-1)

    y_to = models.IntegerField(default=-1)

    option = models.IntegerField(default=-1)

    def get_action(self, state):

        if self.type == 0:
            piece = state.get_piece(Vec(self.x_to, self.y_to))
            return PlaceAction(piece, Vec(self.x_to, self.y_to))

        elif self.type == 1:
            piece = state.previous.get_piece(Vec(self.x_from, self.y_from))
            return MoveAction(piece, Vec(self.x_from, self.y_from),
                Vec(self.x_to, self.y_to))

        elif self.type == 2:
            piece = state.previous.get_piece(Vec(self.x_from, self.y_from))
            return RemoveAction(piece, Vec(self.x_from, self.y_from))

        elif self.type == 3:
            return SelectAction(self.option, Vec(self.x_to, self.y_to))

class ChangeManager(models.Manager):

    def create(self, change, state):
        return super().create(state=state, x=change.pos.x, y=change.pos.y)

class ChangeModel(models.Model):

    changes = ChangeManager()

    state = models.ForeignKey(StateModel, on_delete=models.CASCADE)

    x = models.IntegerField()

    y = models.IntegerField()

    def get_change(self):

        pos = Vec(self.x, self.y)
        old_piece = self.state.previous.get_piece(pos)
        new_piece = self.state.get_piece(pos)

        return Change(pos, old_piece, new_piece)
