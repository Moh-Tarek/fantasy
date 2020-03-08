from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FantasySquad,Player
from django.forms import ModelForm

class UserRegisterForm (UserCreationForm):
    email = forms.EmailField()
    NagwaUnits_CHOICES =(
    ("1", "Product"),
    ("2", "IS"),
    ("3", "Content Creation"),
    ("4", "Content Localization"),
    ("5", "Content Technologist"))
    nagwaTeam = forms.ChoiceField(required=True, label='Unit/Team in Nagwa',choices=NagwaUnits_CHOICES)
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label='Team Name'

        model = User

class SquadSelection (ModelForm):
    class Meta:
        model = FantasySquad
        exclude = ['lastRoundScore','overallScore','user']
    def __init__(self, *args, **kwargs):
        super(SquadSelection, self).__init__(*args, **kwargs)
        self.fields['captinSelected'].queryset = Player.objects.filter(playingRole='Captin')
        self.fields['goalKeeperSelected'].queryset = Player.objects.filter(playingRole='GoalKeeper')
        self.fields['players1Selected'].queryset = Player.objects.filter(playingRole='Player')
