from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FantasySquad,Player,FantasyTeam
from django.forms import ModelForm

class FantasyRegister (ModelForm):
    class Meta:
        model = FantasyTeam
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        self.my_user = kwargs.pop('my_user', None)
        super(FantasyRegister, self).__init__(*args, **kwargs)
        
    
    def save(self, commit=True):
        obj = super(FantasyRegister, self).save(commit=False)
        obj.user = self.my_user
        if commit:
            obj.save()
        return obj

class SquadSelection (ModelForm):
    class Meta:
        model = FantasySquad
        exclude = ['team', 'gameweek']
    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team', None)
        self.gameweek = kwargs.pop('gameweek', None)
        super(SquadSelection, self).__init__(*args, **kwargs)
        self.fields['captainSelected'].queryset = Player.objects.filter(playingRole='Captain')
        self.fields['goalKeeperSelected'].queryset = Player.objects.filter(playingRole='GoalKeeper')
        self.fields['player1Selected'].queryset = Player.objects.filter(playingRole='Player')
        self.fields['player2Selected'].queryset = Player.objects.filter(playingRole='Player')
        self.fields['player3Selected'].queryset = Player.objects.filter(playingRole='Player')
        self.fields['player4Selected'].queryset = Player.objects.filter(playingRole='Player')
        self.fields['player5Selected'].queryset = Player.objects.filter(playingRole='Player')

    def save(self, commit=True):
        obj = super(SquadSelection, self).save(commit=False)
        obj.team = self.team
        obj.gameweek = self.gameweek
        if commit:
            obj.save()
        return obj




