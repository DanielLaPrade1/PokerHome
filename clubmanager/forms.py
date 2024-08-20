from django import forms
from .models import Club, Game, Member, CreatedUser, Tournament
from accounts.models import CustomUser
from django.core.exceptions import ValidationError


class ClubCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input-small', 'placeholder': 'Club Name'}), max_length=20)

    class Meta:
        model = Club
        fields = ('name',)


class AddMemberForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input-game', 'placeholder': 'Username', 'autocomplete': 'off'}), max_length=30)


class CreatedMemberForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input-game m-1', 'placeholder': 'First Name', 'autocomplete': 'off'}), max_length=30)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input-game m-1', 'placeholder': 'Last Name', 'autocomplete': 'off'}), max_length=30)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'input-game m-1', 'placeholder': 'Email (optional)', 'autocomplete': 'off'}), required=False)
    phone = forms.CharField(validators=[CustomUser.phone_regex], widget=forms.TextInput(
        attrs={'class': 'input-game m-1', 'placeholder': 'Phone Number (optional)', 'autocomplete': 'off'}), required=False)

    class Meta:
        model = CreatedUser
        fields = ('first_name', 'last_name', 'email', 'phone')


class GameForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-game', 'placeholder': 'Game Name', 'autocomplete': 'off'}), max_length=30)
    GAME_TYPES = [
        ('', 'Game Type'),
        ('Hold-Em', 'Hold-Em'),
        ('Omaha', 'Omaha'),
        ('Stud', 'Stud'),
        ('High-Low', 'High-Low'),
    ]
    type = forms.ChoiceField(
        choices=GAME_TYPES, label="Game Type", widget=forms.Select(attrs={'class': ''}),)
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
            player_credentials = player.user if player.user else player.created_user
            self.fields[f'{player.id}'] = forms.IntegerField(
                label=f'{player_credentials.first_name} {
                    player_credentials.last_name}',
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
            player_credentials = player.user if player.user else player.created_user
            self.fields[f'{player.id}'] = forms.IntegerField(
                label=f'{player_credentials.first_name} {
                    player_credentials.last_name}',
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
        widget=forms.NumberInput(attrs={'class': 'input-game my-1', 'placeholder': 'Starting Stack'}))
    small_blind = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input-game my-1', 'placeholder': 'Starting Small Blind'}))
    target_duration = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'input-game my-1', 'placeholder': 'Target Duration (Hours)'}))
    blind_duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input-game my-1', 'placeholder': 'Minutes Per Level'}))

    def __init__(self, club, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = club.members.all()

    class Meta:
        model = Tournament
        fields = ("players", 'starting_stack',
                  'small_blind', 'target_duration', 'blind_duration')
