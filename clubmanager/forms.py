from django import forms
from .models import Club, Game, Member, Tournament


class ClubCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input-small', 'placeholder': 'Club Name'}), max_length=20)

    class Meta:
        model = Club
        fields = ('name',)


class AddMemberForm(forms.Form):
    username = forms.CharField(max_length=30)


class GameForm(forms.ModelForm):
    type = forms.CharField(
        widget=forms.TextInput(attrs={'class': '', 'placeholder': 'Type'}), max_length=30)
    buy_in = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': '', 'placeholder': 'Buy In Amount'}))
    players = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, club, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = club.members.all()

    class Meta:
        model = Game
        fields = ("type", "buy_in", 'players')


class TournamentForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    starting_stack = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': '', 'placeholder': 'Starting Stack'}))
    small_blind = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': '', 'placeholder': 'Starting Small Blind'}))
    target_duration = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': '', 'placeholder': 'Target Duration (Hours)'}))
    blind_duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': '', 'placeholder': 'Minutes Per Level'}))

    def __init__(self, club, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = club.members.all()

    class Meta:
        model = Tournament
        fields = ("players", 'starting_stack',
                  'small_blind', 'target_duration', 'blind_duration')
