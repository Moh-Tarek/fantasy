from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FantasySquad,Player,FantasyTeam
from django.forms import ModelForm

class FantasyRegister (ModelForm):
    class Meta:
        model = FantasyTeam
        exclude = ['user','lastRoundScore','overallScore']


class SquadSelection (ModelForm):
    class Meta:
        model = FantasySquad
        exclude = ['lastRoundScore','overallScore','user']
    def __init__(self, *args, **kwargs):
        super(SquadSelection, self).__init__(*args, **kwargs)
        self.fields['captinSelected'].queryset = Player.objects.filter(playingRole='Captin')
        self.fields['goalKeeperSelected'].queryset = Player.objects.filter(playingRole='GoalKeeper')
        self.fields['players1Selected'].queryset = Player.objects.filter(playingRole='Player')



