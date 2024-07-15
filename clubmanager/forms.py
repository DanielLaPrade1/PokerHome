from django import forms
from .models import Club, Game, Member, Tournament
from django.core.exceptions import ValidationError


class ClubCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input-small', 'placeholder': 'Club Name'}), max_length=20)

    class Meta:
        model = Club
        fields = ('name',)


class AddMemberForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input-game', 'placeholder': 'Type', 'autocomplete': 'off'}), max_length=30)


class GameForm(forms.ModelForm):
    type = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-game', 'placeholder': 'Type', 'autocomplete': 'off'}), max_length=30)
    buy_in = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'input-game', 'placeholder': 'Buy In Amount', 'autocomplete': 'off'}))
    players = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    def __init__(self, club, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = club.members.all()

    class Meta:
        model = Game
        fields = ("type", "buy_in", 'players')


class GameBuyInEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game')
        super(GameBuyInEditForm, self).__init__(*args, **kwargs)

        for player in game.players.all():
            self.fields[f'{player.id}'] = forms.IntegerField(
                label=f'{player.user.first_name} {
                    player.user.last_name}',
                required=True,
                initial=game.player_buy_ins[player.id],
                widget=forms.NumberInput(
                    attrs={'class': 'player-score-box input-game', 'autocomplete': 'off'})
            )


class GameScoresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game')
        super(GameScoresForm, self).__init__(*args, **kwargs)

        for player in game.players.all():
            self.fields[f'{player.id}'] = forms.IntegerField(
                label=f'{player.user.first_name} {
                    player.user.last_name}',
                required=True,
                initial=game.player_buy_ins[player.id],
                widget=forms.NumberInput(
                    attrs={'class': 'player-score-box input-game', 'autocomplete': 'off'})
            )


class TournamentForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    starting_stack = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input-game', 'placeholder': 'Starting Stack'}))
    small_blind = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input-game', 'placeholder': 'Starting Small Blind'}))
    target_duration = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'input-game', 'placeholder': 'Target Duration (Hours)'}))
    blind_duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input-game', 'placeholder': 'Minutes Per Level'}))

    def __init__(self, club, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = club.members.all()

    class Meta:
        model = Tournament
        fields = ("players", 'starting_stack',
                  'small_blind', 'target_duration', 'blind_duration')
