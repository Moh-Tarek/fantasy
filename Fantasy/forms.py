from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FantasySquad,Player,FantasyTeam
from django.forms import ModelForm
import collections

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

    def is_valid(self):
        valid = super(SquadSelection, self).is_valid()
        if valid:
            selected_palyers = [
                self.cleaned_data['captainSelected'],
                self.cleaned_data['goalKeeperSelected'],
                self.cleaned_data['player1Selected'],
                self.cleaned_data['player2Selected'],
                self.cleaned_data['player3Selected'],
                self.cleaned_data['player4Selected'],
                self.cleaned_data['player5Selected']
            ]
            # 1. Check unique selections
            duplicates = [item for item, count in collections.Counter(selected_palyers).items() if count > 1]
            if len(duplicates) > 0:
                c = 0
                for p in seen:
                    if c == 0:
                        self.add_error(None, f'You have selected {p} more than once! Do you like him that much?! I don\'t care, please make sure to select him once.')
                    else:
                        self.add_error(None, f'Same applies for {p}!')
                    c += 1
                valid = False
                return valid
            # 2. check that no more than 2 players are selected from the same team
            selected_palyers_teams = [p.teamName for p in selected_palyers]
            selected_palyers_teams_dict = {i:selected_palyers_teams.count(i) for i in selected_palyers_teams}
            c = 0
            for k,v in selected_palyers_teams_dict.items():
                if v > 2:
                    affected_players = [p.playerName for p in selected_palyers if p.teamName == k]
                    if c == 0:
                        self.add_error(None, f'Don\'t Be Greedy! You have selected {v} palyers: {affected_players} from "{k}" team. It is not permitted to select more than 2 players from the same team.')
                    else:
                        self.add_error(None, f'Same applies for the {v} players: {affected_players} from "{k}" team!')
                    c += 1
                    valid = False
        return valid


    def save(self, commit=True):
        obj = super(SquadSelection, self).save(commit=False)
        obj.team = self.team
        obj.gameweek = self.gameweek
        if commit:
            obj.save()
        return obj




