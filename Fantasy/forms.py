from .models import FantasySquad, Fixture, FootballTeam, GameweekSetting, Player, Score
from django.forms import ModelForm
import collections

# class FantasyRegister (ModelForm):
#     class Meta:
#         model = Team
#         exclude = ['user']

#     def __init__(self, *args, **kwargs):
#         self.my_user = kwargs.pop('my_user', None)
#         super(FantasyRegister, self).__init__(*args, **kwargs)
        
    
#     def save(self, commit=True):
#         obj = super(FantasyRegister, self).save(commit=False)
#         obj.user = self.my_user
#         if commit:
#             obj.save()
#         return obj

class GameweekSettingForm(ModelForm):
    class Meta:
        model = GameweekSetting
        fields = '__all__'

class ScoreForm(ModelForm):
    class Meta:
        model = Score
        exclude = ['player', 'fixture']
        # fields = '__all__'

class LimitedScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ('played',)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.goal = 0
        obj.assist = 0
        obj.own_goal = 0
        obj.yellow_card = False
        obj.red_card = False
        obj.clean_sheet = False
        obj.penalty_saved = 0
        obj.penalty_missed = 0

        if commit:
            obj.save()
        return obj

class FixtureWithdrawForm(ModelForm):
    class Meta:
        model = Fixture
        fields = ('withdrawn_team',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            teams = []
            team1 = self.instance.team1
            if team1:
                teams.append(team1.pk)
            team2 = self.instance.team2
            if team2:
                teams.append(team2.pk)
            self.fields['withdrawn_team'].queryset = FootballTeam.objects.filter(pk__in=teams)


class SquadSelection(ModelForm):
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
                for p in duplicates:
                    if c == 0:
                        self.add_error(None, f'You have selected {p} more than once! Do you like him that much?! I don\'t care, please make sure to select him once.')
                    else:
                        self.add_error(None, f'Same applies for {p}!')
                    c += 1
                valid = False
                return valid
            # 2. check that no more than 2 players are selected from the same team
            selected_palyers_teams = [p.team for p in selected_palyers]
            selected_palyers_teams_dict = {i:selected_palyers_teams.count(i) for i in selected_palyers_teams}
            c = 0
            for k,v in selected_palyers_teams_dict.items():
                if v > 2:
                    affected_players = [p.playerName for p in selected_palyers if p.team == k]
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




