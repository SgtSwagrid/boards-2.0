from django.db import models
from django.contrib.auth.models import User
from .games.games import games
from datetime import time
import random

class BoardManager(models.Manager):

    def create(self, game_id):

        code = hex(random.randint(0, 1048575))[2:].zfill(5).upper()
        state = State.objects.create(game_id=game_id, turn=1)
        board = super().create(game_id=game_id, code=code, state=state)
        game = games[game_id]

        for x in range(0, game.width):
            for y in range(0, game.height):
                type, owner_id = board.game().initial(x, y)
                if type: Piece.objects.create(
                    state=state, type_id=type.id, owner_id=owner_id, x=x, y=y)
        return board

class Board(models.Model):

    game_id = models.IntegerField()

    code = models.CharField(max_length=5)

    state = models.ForeignKey('State',
        on_delete=models.SET_NULL, null=True, blank=True)

    stage = models.IntegerField(default=0)

    time = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ['-time']

    def __str__(self): return self.code + " " + self.game().name

    boards = BoardManager()

    def place_piece(self, player_id, x, y, type=None):

        if not type: type = self.game().types[0]

        if self.game().place_valid(self.state, self.state.pieces(),
                                   type, player_id, x, y):
            self.state = self.state.next()
            self.game().place_piece(self.state, self.state.pieces(),
                                    type, player_id, x, y)
            if self.state.outcome != -1: self.stage = 2
            self.state.save()
            self.save()
            return True
        else: return False

    def move_piece(self, x_from, y_from, x_to, y_to):

        if self.game().move_valid(self.state, self.state.pieces(),
                                  x_from, y_from, x_to, y_to):
            self.state = self.state.next()
            self.game().move_piece(self.state, self.state.pieces(),
                                   x_from, y_from, x_to, y_to)
            if self.state.outcome != -1: self.stage = 2
            self.state.save()
            self.save()
            return True
        else: return False

    def remove_piece(self, x, y):

        if self.game().remove_valid(self.state, self.state.pieces(), x, y):
            self.state = self.state.next()
            self.game().remove_piece(self.state, self.state.pieces(), x, y)
            if self.state.outcome != -1: self.stage = 2
            self.state.save()
            self.save()
            return True
        else: return False

    def selectable(self, x, y):
        return self.game().selectable(self.state, self.state.pieces(), x, y)

    def current(self, player):
        return player and player.order == self.state.turn

    def players(self):
        return Player.objects.filter(board=self)

    def player(self, user):
        return self.players().filter(user=user).first()\
            if user.is_authenticated else None

    def game(self):
        return games[self.game_id]

    def messages(self):
        return Message.objects.filter(board=self)

    def users(self):
        return map(lambda p: p.user, self.players())

    def join(self, user):
        Player.objects.create(user=user, board=self,
                order=self.players().count()+1)

    def start(self):
        self.stage = 1
        self.save()

    def to_dictionary(self):
        return {
            'game': self.game(),
            'code': self.code,
            'state': self.state,
            'players': self.players(),
            'stage': self.stage,
            'time': self.time,
            'messages': self.messages()
        }

class Player(models.Model):

    user = models.ForeignKey(User,
        on_delete=models.SET_NULL, null=True)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)

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

class State(models.Model):

    game_id = models.IntegerField()

    turn = models.IntegerField(default=1)

    stage = models.IntegerField(default=0)

    ply = models.IntegerField(default=0)

    previous = models.ForeignKey('State',
        on_delete=models.CASCADE, null=True)

    outcome = models.IntegerField(default=-1)

    def next(self):

        state = State.objects.create(
            game_id=self.game_id,
            turn=self.turn,
            stage=self.stage,
            ply=self.ply,
            previous=self,
            outcome=self.outcome
        )

        for row in self.pieces():
            for piece in row:
                if piece: piece.next(state)
        return state

    def end_stage(self, skip=1):
        self.stage = self.stage + skip
        self.save()

    def end_turn(self, skip=1):
        self.turn = self.turn % self.game().players + skip
        self.ply = self.ply + 1
        self.stage = 0
        self.save()

    def end_game(self, winner=0):
        self.outcome = winner
        self.save()

    def set_piece(self, type_id, owner_id, x, y):

        Piece.objects.filter(state=self, x=x, y=y).delete()

        if type_id != -1: Piece.objects.create(
            state=self,
            type_id=type_id,
            x=x, y=y,
            owner_id=owner_id
        )

        Change.objects.create(state=self, x=x, y=y)

    def place_piece(self, type, owner_id, x, y):
        self.set_piece(type.id, owner_id, x, y)

    def move_piece(self, x_from, y_from, x_to, y_to):
        piece = Piece.objects.filter(state=self, x=x_from, y=y_from).get()
        self.set_piece(-1, 0, x_from, y_from)
        self.set_piece(piece.type_id, piece.owner_id, x_to, y_to)

    def remove_piece(self, x, y):
        self.set_piece(-1, 0, x, y)

    def game(self):
        return games[self.game_id]

    def pieces(self):

        piece_set = Piece.objects.filter(state=self)
        pieces = []

        for x in range(0, self.game().width):
            col_set = piece_set.filter(x=x)
            col = []

            for y in range(0, self.game().height):
                col.append(col_set.filter(y=y).first())
            pieces.append(col)
        return pieces

    def changes(self):
        return Change.objects.filter(state=self, state__ply=self.ply)

    def to_dictionary(self):
        return {
            'game': self.game(),
            'turn': self.turn,
            'stage': self.stage,
            'previous': self.previous,
            'number': self.number,
            'outcome': self.outcome,
            'pieces': self.pieces()
        }

class Change(models.Model):

    state = models.ForeignKey(State, on_delete=models.CASCADE)

    x = models.IntegerField()

    y = models.IntegerField()

class Piece(models.Model):

    state = models.ForeignKey(State,
        on_delete=models.CASCADE)

    type_id = models.IntegerField()

    owner_id = models.IntegerField()

    x = models.IntegerField()

    y = models.IntegerField()

    class Meta: ordering = ['state']

    def __str__(self): return self.state.board.code + ":"\
            + str(self.state.number) + ":" + str(self.id)

    def next(self, state):
        return Piece.objects.create(
            state=state,
            type_id=self.type_id,
            owner_id=self.owner_id,
            x=self.x,
            y=self.y
        )

    def type(self):
        return self.state.game().types[self.type_id]

    def texture(self):
        return self.type().texture(self.owner_id)

    def owner(self, board):
        return board.players()[self.owner_id-1]

    def to_dictionary(self):
        return {
            'state': self.state,
            'type': self.type(),
            'owner_id': self.owner_id,
            'x': self.x,
            'y': self.y,
            'texture': self.texture()
        }

class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.CharField(max_length=500)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    time = models.DateTimeField(auto_now=True)

    class Meta: ordering = ['board', '-time']

    def __str__(self): return self.board.code + ":" + str(self.id)