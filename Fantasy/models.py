from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import DateTimeField
from .constants import (
    PLAYED_POINTS, 
    GOAL_POINTS, 
    ASSIST_POINTS,
    OWN_GOAL_POINTS, 
    YELLOW_CARD_POINTS, 
    RED_CARD_POINTS, 
    CLEAN_SHEET_POINTS,
    PENALTY_SAVED_POINTS, 
    PENALTY_MISSED_POINTS
)
from django.db.models import Model, Manager, QuerySet, ForeignKey, CharField, IntegerField, BooleanField, ImageField, DateTimeField, CASCADE, URLField
from django.db.models import Sum, Count, Case, When, Value
from django.contrib.auth.models import User


class GameweekSetting(Model):
    active_gameweek = IntegerField()
    gameweek_deadline = DateTimeField()
    max_players_same_team = IntegerField(default=2)

class Team(User):
    class Meta:
        proxy = True
        
    @cached_property
    def total_team_score(self):
        team_score = 0
        for s in self.squads.all():
            team_score += s.total_squad_score
        return team_score

    @cached_property
    def last_gameweek_team_score(self):
        try:
            last_gameweek = GameweekSetting.objects.last().active_gameweek - 1
        except:
            last_gameweek = 0
        last_gameweek_squad = self.squads.filter(gameweek=last_gameweek)
        if last_gameweek_squad:
            return last_gameweek_squad[0].total_squad_score
        return None

class Group(Model):
    name = CharField(max_length=1, unique=True)

    def __str__(self):
        return "Group " + self.name

class FootballTeam(Model):
    name = CharField(max_length=100, unique=True)
    group = ForeignKey(Group, on_delete=CASCADE, related_name='teams', null=True)
    color = CharField(max_length=20, default="royalblue")

    def __str__(self):
        return self.name

    @cached_property
    def short_name(self):
        # from googletrans import Translator
        # detector = Translator()
        # name_lang = detector.detect(self.name[0]).lang
        name_lang = "ar"
        if self.name[0].lower() in "abcdefghijklmnopqrstuvwxyz":
            name_lang = "en"
        name = self.name.split(" ")
        short_name = ""
        if name_lang == "en":
            if len(name) > 1:
                for n in name:
                    if len(n) > 2:
                        short_name += n[0]
                    else:
                        short_name += n
                short_name = short_name.upper()
            else:
                short_name = (name[0][0] + name[0][1]).upper()
        elif name_lang == "ar":
            new_name = []
            for n in name:
                if n[:2] == 'ال':
                    new_name.append(n[2:])
                else:
                    new_name.append(n)
            if len(new_name) > 1:
                short_name = new_name[0][0] + " " + new_name[1][0]
            else:
                short_name = new_name[0][:2]
        else:
            short_name = self.name
        return short_name

    @cached_property
    def fixtures(self):
        hf = self.home_fixtures.all()
        af = self.away_fixtures.all()
        return hf, af

    @cached_property
    def group_fixtures(self):
        hf = self.home_fixtures.filter(stage="G")
        af = self.away_fixtures.filter(stage="G")
                

class Player(Model):
    playerName = CharField(max_length=100, unique=True)
    image = ImageField(
        default='defaultplayer.jpg', upload_to='profile_pics')
    team = ForeignKey(FootballTeam, on_delete=CASCADE, related_name='players')
    playingRoleChoices = (
        ('Captain', 'Captain'),
        ('GoalKeeper', 'GoalKeeper'),
        ('Player', 'Player'),
    )
    playingRole = CharField(max_length=100, choices=playingRoleChoices)

    @cached_property
    def total_player_score(self):
        total_player_score = 0
        for s in self.player_scores.all():
            total_player_score += s.total_score
        return total_player_score

    @cached_property
    def last_gameweek_player_score(self):
        try:
            last_gameweek = GameweekSetting.objects.last().active_gameweek - 1
        except:
            last_gameweek = 0
        last_gameweek_score = self.player_scores.filter(fixture__gameweek=last_gameweek)
        if last_gameweek_score:
            return last_gameweek_score[0].total_score
        return 0

    @cached_property
    def last_gameweek_player_score_objs(self):
        try:
            last_gameweek = GameweekSetting.objects.last().active_gameweek - 1
        except:
            last_gameweek = 0
        last_gameweek_score = self.player_scores.filter(fixture__gameweek=last_gameweek)
        return last_gameweek_score

    def __str__(self):
        return f"{self.playerName} ({self.team})"

    class Meta:
        ordering = ('playerName', )

class FantasySquad(Model):
    team = ForeignKey(
        Team, on_delete=CASCADE, related_name="squads")
    captainSelected = ForeignKey(
        Player, on_delete=CASCADE, related_name='C', verbose_name="Captain")
    goalKeeperSelected = ForeignKey(
        Player, on_delete=CASCADE, related_name='GK', verbose_name="GoalKeeper")
    player1Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P1', verbose_name="Player 1")
    player2Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P2', verbose_name="Player 2")
    player3Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P3', verbose_name="Player 3")
    player4Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P4', verbose_name="Player 4")
    player5Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P5', verbose_name="Player 5")
    gameweek = IntegerField()

    class Meta:
        unique_together = ['team', 'gameweek']

    def get_player_score(self, player):
        score_objects = player.player_scores.filter(fixture__gameweek=self.gameweek)
        if score_objects:
            score = 0
            for s in score_objects:
                score += s.total_score
            return score
        return None

    @cached_property
    def captainSelected_score(self):
        c = self.get_player_score(self.captainSelected)
        if c:
            c *= 2
        return c

    @cached_property
    def goalKeeperSelected_score(self):
        return self.get_player_score(self.goalKeeperSelected)

    @cached_property
    def player1Selected_score(self):
        return self.get_player_score(self.player1Selected)

    @cached_property
    def player2Selected_score(self):
        return self.get_player_score(self.player2Selected)

    @cached_property
    def player3Selected_score(self):
        return self.get_player_score(self.player3Selected)

    @cached_property
    def player4Selected_score(self):
        return self.get_player_score(self.player4Selected)

    @cached_property
    def player5Selected_score(self):
        return self.get_player_score(self.player5Selected)

    @cached_property
    def total_squad_score(self):
        total_squad_score = 0
        scores = [
            self.captainSelected_score,
            self.goalKeeperSelected_score,
            self.player1Selected_score,
            self.player2Selected_score,
            self.player3Selected_score,
            self.player4Selected_score,
            self.player5Selected_score
        ]
        for s in scores:
            if not s is None:
                total_squad_score += s
        return total_squad_score

    def __str__(self):
        return f"{self.team} - GW{self.gameweek}" 
        
# class ScoreManager(Manager):
class ScoreQuerySet(QuerySet):
    def get_goals(self):
        return self.filter(goal__gt=0).order_by('-goal').values_list('player__playerName', 'goal')
    def get_goals_sum(self):
        return self.aggregate(t=Sum('goal'))['t'] or 0

    def get_assists(self):
        return self.filter(assist__gt=0).order_by('-assist').values_list('player__playerName', 'assist')
    def get_assists_sum(self):
        return self.aggregate(t=Sum('assist'))['t'] or 0

    def get_own_goals(self):
        return self.filter(own_goal__gt=0).order_by('-own_goal').values_list('player__playerName', 'own_goal')
    def get_own_goals_sum(self):
        return self.aggregate(t=Sum('own_goal'))['t'] or 0

    def get_yellow_cards(self):
        return self.filter(yellow_card=True).values_list('player__playerName', 'yellow_card')
    def get_yellow_cards_sum(self):
        return self.aggregate(t=Count(Case(When(yellow_card=True, then=Value(1)))))['t']

    def get_red_cards(self):
        return self.filter(red_card=True).values_list('player__playerName', 'red_card')
    def get_red_cards_sum(self):
        return self.aggregate(t=Count(Case(When(red_card=True, then=Value(1)))))['t']

    def get_clean_sheets(self):
        return self.filter(clean_sheet=True).values_list('player__playerName', 'clean_sheet')
    def get_clean_sheets_sum(self):
        return self.aggregate(t=Count(Case(When(clean_sheet=True, then=Value(1)))))['t']

    def get_penalties_saved(self):
        return self.filter(penalty_saved__gt=0).order_by('-penalty_saved').values_list('player__playerName', 'penalty_saved')
    def get_penalties_saved_sum(self):
        return self.aggregate(t=Sum('penalty_saved'))['t'] or 0

    def get_penalties_missed(self):
        return self.filter(penalty_missed__gt=0).order_by('-penalty_missed').values_list('player__playerName', 'penalty_missed')
    def get_penalties_missed_sum(self):
        return self.aggregate(t=Sum('penalty_missed'))['t'] or 0

class Score(Model):
    player = ForeignKey(
        Player, on_delete=CASCADE, related_name="player_scores")
    fixture = ForeignKey('Fixture', on_delete=CASCADE, related_name="scores")

    played = BooleanField(default=False)
    goal = IntegerField(default=0)
    assist = IntegerField(default=0)
    own_goal = IntegerField(default=0)
    yellow_card = BooleanField(default=False)
    red_card = BooleanField(default=False)
    clean_sheet = BooleanField(default=False)
    penalty_saved = IntegerField(default=0)
    penalty_missed = IntegerField(default=0)

    # objects = ScoreManager()
    objects = ScoreQuerySet.as_manager()

    @cached_property
    def total_score(self):
        total_score = 0
        if self.played:
            total_score = PLAYED_POINTS * self.played \
                + GOAL_POINTS * self.goal \
                + ASSIST_POINTS * self.assist \
                + OWN_GOAL_POINTS * self.own_goal \
                + PENALTY_SAVED_POINTS * self.penalty_saved \
                + PENALTY_MISSED_POINTS * self.penalty_missed

            if self.red_card:
                total_score += RED_CARD_POINTS

            if self.yellow_card and not self.red_card:
                total_score += YELLOW_CARD_POINTS

            # if self.player.playingRole == "Captain":
            #     total_score *= 2

            # if self.player.playingRole == "GoalKeeper" and self.clean_sheet:
            #     total_score += CLEAN_SHEET_POINTS

        # add clean sheet points to the goalkeeper even if he didn't play the match
        # doesn't make sense at all, but I added it for M. Tarek
        if self.player.playingRole == "GoalKeeper" and self.clean_sheet:
            total_score += CLEAN_SHEET_POINTS

        return total_score

    class Meta:
        unique_together = ['player', 'fixture']

    def clean(self):
        if self.player not in self.fixture.players:
            raise ValidationError(_('The selected player doesn\'t play in any of the two teams of the selected fixture'))
        
    def __str__(self):
        return f"{self.player.playerName} - {self.fixture}"


class Fixture(Model):
    team1 = ForeignKey(FootballTeam, on_delete=CASCADE, related_name="home_fixtures", null=True, blank=True)
    team1_representation = CharField(max_length=100, null=True, blank=True)
    team1_penalties = IntegerField(null=True, blank=True)
    team2 = ForeignKey(FootballTeam, on_delete=CASCADE, related_name="away_fixtures", null=True, blank=True)
    team2_representation = CharField(max_length=100, null=True, blank=True)
    team2_penalties = IntegerField(null=True, blank=True)
    gameweek = IntegerField()
    url = URLField(max_length=100,null=True, blank=True ,unique=True)
    stage = CharField(choices=[
        ('G', 'Group'), 
        ('QF', 'Quarter-Final'), 
        ('SF', 'Semi-Final'), 
        ('3P', '3rd Place Playoff'),
        ('F', 'Final')
    ], max_length=20, default='G')
    date = DateTimeField()
    withdrawn_team = ForeignKey(
        FootballTeam, on_delete=CASCADE, related_name="withdraw_fixtures", null=True, blank=True,
        help_text="If one of the teams withdrew from the match, select it and the other team will be considered as the winner of the match with score 2-0"
    )
    
    @cached_property
    def team1_verbose_name(self):
        if self.team1:
            return self.team1
        return self.team1_representation

    @cached_property
    def team2_verbose_name(self):
        if self.team2:
            return self.team2
        return self.team2_representation

    @cached_property
    def team1_scores(self):
        return Score.objects.filter(fixture=self, player__team=self.team1)

    @cached_property
    def team2_scores(self):
        return Score.objects.filter(fixture=self, player__team=self.team2)

    def _result(self):
        team1_result, team2_result = None, None
        if self.withdrawn_team:
            if self.withdrawn_team == self.team1:
                team1_result, team2_result = 0, 2
            elif self.withdrawn_team == self.team2:
                team1_result, team2_result = 2, 0
            return team1_result, team2_result
        team1_scores = self.team1_scores
        team2_scores = self.team2_scores
        if team1_scores or team2_scores:
            team1_result = 0
            team2_result = 0
            for s1 in team1_scores:
                team1_result += s1.goal
                team2_result += s1.own_goal
            for s2 in team2_scores:
                team2_result += s2.goal
                team1_result += s2.own_goal
        return team1_result, team2_result

    @cached_property
    def team1_result(self):
        return self._result()[0]
    
    @cached_property
    def team2_result(self):
        return self._result()[1]

    @cached_property
    def all_result(self):
        return self._result()

    @cached_property
    def players(self):
        a = list(self.team1.players.all())
        b = list(self.team2.players.all())
        return a + b

    # @cached_property
    # def team2_goals(self):
    #     goals = None
    #     scores = Score.objects.filter(fixture=self, player__team=self.team2)
    #     if scores:
    #         goals = 0
    #         for s in scores:
    #             goals += s.goal
    #     return goals

    class Meta:
        ordering = ['gameweek', 'date']
        unique_together = ['gameweek', 'team1', 'team2']

    @cached_property
    def is_finished(self):
        if self.withdrawn_team or (self.team1_result != None and self.team2_result != None):
            return True
        return False
    
    def __str__(self):
        return f"GW{self.gameweek}: {self.team1_verbose_name} vs {self.team2_verbose_name}"
    

# class FantasyTeam(Model):
#     user = ForeignKey(User, on_delete=CASCADE)
#     FantasyPlayerName = CharField(max_length=100)
#     FantasyTeamName = CharField(max_length=100)
#     nagwaID = IntegerField(null=True, blank=True)

#     @property
#     def total_team_score(self):
#         team_score = 0
#         for s in self.squads.all():
#             team_score += s.total_squad_score
#         return team_score

#     @property
#     def last_gameweek_team_score(self):
#         last_gameweek = int(os.getenv('GAMEWEEK')) - 1
#         last_gameweek_squad = self.squads.filter(gameweek=last_gameweek)
#         if last_gameweek_squad:
#             return last_gameweek_squad[0].total_squad_score
#         return None