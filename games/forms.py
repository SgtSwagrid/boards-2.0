from django import forms
from games.games.common.games import games

class GameForm(forms.Form):

    game = forms.ChoiceField(
        choices=map(lambda g: (g.id, g.name), games.values()))

    opponent = forms.CharField()