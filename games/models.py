from django.db import models
from django.contrib.auth.models import User
from games.games.common.games import games
from datetime import time
import random

from .games.common.game import *
from .games.common.state import *

class BoardManager(models.Manager):

    def create(self, game):

        code = hex(random.randint(0, 1048575))[2:].zfill(5).upper()
        state = StateModel.states.from_state(game.setup(), previous=None)
        board = super().create(game_id=game.id, code=code, state=state)
        return board

class BoardModel(models.Model):

    boards = BoardManager()

    game_id = models.IntegerField()

    code = models.CharField(max_length=5)

    state = models.ForeignKey('StateModel',
        on_delete=models.SET_NULL, null=True, blank=True)

    status = models.IntegerField(default=0)

    time = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ['-time']

    def __str__(self): return self.code + " " + self.game().name

    def input(self, display, input):
        result, display = self.game().input(self.state.to_state(), display, input)
        if result:
            self.state = StateModel.states.from_state(result, previous=self.state)
            if self.state.outcome != -2: self.status = 2
            self.save()
        return result, display

    def current(self, player):
        return player and player.order == self.state.current

    def players(self):
        return PlayerModel.objects.filter(board=self)

    def player(self, user):
        return self.players().filter(user=user).first()\
            if user.is_authenticated else None

    def game(self):
        return games[self.game_id]

    def users(self):
        return map(lambda p: p.user, self.players())

    def join(self, user):
        order = self.players().count()
        PlayerModel.objects.create(user=user, board=self,
            order=order, leader=order == 0)

    def start(self):
        self.status = 1
        self.save()

    def to_dictionary(self):
        return {
            'game': self.game(),
            'code': self.code,
            'state': self.state,
            'players': self.players(),
            'status': self.status,
            'time': self.time
        }

class PlayerModel(models.Model):

    user = models.ForeignKey(User,
        on_delete=models.SET_NULL, null=True)

    board = models.ForeignKey(BoardModel, on_delete=models.CASCADE)

    order = models.IntegerField()

    score = models.IntegerField(default=0)

    leader = models.BooleanField(default=False)

    time = models.TimeField(default=time(0, 0, 0))

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

class StateManager(models.Manager):

    def from_state(self, state, previous):

        state_model = super().create(
            game_id=state.game.id,
            current=state.turn.current,
            stage=state.turn.stage,
            ply=state.turn.ply,
            outcome=-2 if not state.outcome.finished else
                -1 if state.outcome.draw else
                state.outcome.winner.id,
            previous=previous)

        for player in state.players:
            PlayerStateModel.players.from_player(player, state_model)

        for col in state.pieces:
            for piece in col:
                if piece: PieceModel.pieces.from_piece(piece, state_model)

        for x, y in state.changes:
            ChangeModel.objects.create(state=state_model, x=x, y=y)

        return state_model

class StateModel(models.Model):

    states = StateManager()

    game_id = models.IntegerField()

    current = models.IntegerField(default=0)

    stage = models.IntegerField(default=0)

    ply = models.IntegerField(default=0)

    outcome = models.IntegerField(default=-2)

    previous = models.ForeignKey('StateModel',
        on_delete=models.CASCADE, null=True)

    def to_state(self):

        game = games[self.game_id]

        players = [p.to_player() for p in
            PlayerStateModel.players.filter(state=self)]

        def to_piece(piece): return piece.to_piece() if piece else None
        pieces = [[to_piece(PieceModel.pieces
            .filter(state=self, x=x, y=y).first())
            for y in range(0, game.height)]
                for x in range(0, game.width)]

        turn = Turn(
            current=self.current,
            stage=self.stage,
            ply=self.ply)

        outcome = Outcome(
            finished=self.outcome > -2,
            winner=players[self.outcome] if self.outcome > -1 else None,
            draw=self.outcome == -1)

        changes = {(change.x, change.y)
            for change in ChangeModel.objects.filter(state=self)}

        return State(
            game=games[self.game_id],
            players=players,
            pieces=pieces,
            turn=turn,
            outcome=outcome,
            changes=changes,
            previous=self.previous_state)

    def previous_state(self):
        return self.previous.to_state() if self.previous else None

class PlayerStateManager(models.Manager):

    def from_player(self, player, state):
        return super().create(
            state=state,
            order=player.order,
            score=player.score)

class PlayerStateModel(models.Model):

    players = PlayerStateManager()

    state = models.ForeignKey(StateModel, on_delete=models.CASCADE)

    order = models.IntegerField()

    score = models.IntegerField(default=0)

    class Meta: ordering = ['state', 'order']

    def to_player(self):
        return PlayerState(
            order=self.order,
            score=self.score)

class PieceManager(models.Manager):

    def from_piece(self, piece, state):
        return super().create(
            state=state,
            type=piece.type.id,
            owner=piece.owner,
            x=piece.x,
            y=piece.y)

class PieceModel(models.Model):

    pieces = PieceManager()

    state = models.ForeignKey(StateModel, on_delete=models.CASCADE)

    type = models.IntegerField()

    owner = models.IntegerField()

    x = models.IntegerField()

    y = models.IntegerField()

    class Meta: ordering = ['state']

    def to_piece(self):
        return Piece(
            type=games[self.state.game_id].types[self.type],
            owner=self.owner,
            x=self.x,
            y=self.y)

class ChangeModel(models.Model):

    state = models.ForeignKey(StateModel, on_delete=models.CASCADE)

    x = models.IntegerField()

    y = models.IntegerField()