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
        super(SquadSelection, self).__init__(*args, **kwargs)
        self.fields['captainSelected'].queryset = Player.objects.filter(playingRole='Captin')
        self.fields['goalKeeperSelected'].queryset = Player.objects.filter(playingRole='GoalKeeper')
        self.fields['player1Selected'].queryset = Player.objects.filter(playingRole='Player')



