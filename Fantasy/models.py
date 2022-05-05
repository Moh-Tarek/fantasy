from .constants import GOAL_POINTS, ASSIST_POINTS, YELLOW_CARD_POINTS, RED_CARD_POINTS, CLEAN_SHEET_POINTS, \
    PENALTY_SAVED_POINTS, PENALTY_MISSED_POINTS

from django.db.models import Model, ForeignKey, CharField, IntegerField, BooleanField, ImageField, CASCADE
from django.contrib.auth.models import User

import os


class Team(User):
    class Meta:
        proxy = True
        
    @property
    def total_team_score(self):
        team_score = 0
        for s in self.squads.all():
            team_score += s.total_squad_score
        return team_score

    @property
    def last_gameweek_team_score(self):
        last_gameweek = int(os.getenv('GAMEWEEK')) - 1
        last_gameweek_squad = self.squads.filter(gameweek=last_gameweek)
        if last_gameweek_squad:
            return last_gameweek_squad[0].total_squad_score
        return None


class Player(Model):
    playerName = CharField(max_length=100, unique=True)
    image = ImageField(
        default='defaultplayer.jpg', upload_to='profile_pics')
    teamName = CharField(max_length=100)
    playingRoleChoices = (
        ('Captain', 'Captain'),
        ('GoalKeeper', 'GoalKeeper'),
        ('Player', 'Player'),
    )
    playingRole = CharField(max_length=100, choices=playingRoleChoices)

    @property
    def total_player_score(self):
        total_player_score = 0
        for s in self.player_scores.all():
            total_player_score += s.total_score
        return total_player_score

    @property
    def last_gameweek_player_score(self):
        last_gameweek = int(os.getenv('GAMEWEEK')) - 1
        last_gameweek_score = self.player_scores.filter(gameweek=last_gameweek)
        if last_gameweek_score:
            return last_gameweek_score[0].total_score
        return None

    def __str__(self):
        return self.playerName


class FantasySquad(Model):
    team = ForeignKey(
        Team, on_delete=CASCADE, related_name="squads")
    captainSelected = ForeignKey(
        Player, on_delete=CASCADE, related_name='C')
    goalKeeperSelected = ForeignKey(
        Player, on_delete=CASCADE, related_name='GK')
    player1Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P1')
    player2Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P2')
    player3Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P3')
    player4Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P4')
    player5Selected = ForeignKey(
        Player, on_delete=CASCADE, related_name='P5')
    gameweek = IntegerField()

    class Meta:
        unique_together = ['team', 'gameweek']

    def get_player_score(self, player):
        score_obj = player.player_scores.filter(gameweek=self.gameweek)
        if score_obj:
            return score_obj[0].total_score
        return None

    @property
    def captainSelected_score(self):
        return self.get_player_score(self.captainSelected)

    @property
    def goalKeeperSelected_score(self):
        return self.get_player_score(self.goalKeeperSelected)

    @property
    def player1Selected_score(self):
        return self.get_player_score(self.player1Selected)

    @property
    def player2Selected_score(self):
        return self.get_player_score(self.player2Selected)

    @property
    def player3Selected_score(self):
        return self.get_player_score(self.player3Selected)

    @property
    def player4Selected_score(self):
        return self.get_player_score(self.player4Selected)

    @property
    def player5Selected_score(self):
        return self.get_player_score(self.player5Selected)

    @property
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


class Score(Model):
    player = ForeignKey(
        Player, on_delete=CASCADE, related_name="player_scores")
    gameweek = IntegerField()

    goal = IntegerField(default=0)
    assist = IntegerField(default=0)
    yellow_card = BooleanField(default=False)
    red_card = BooleanField(default=False)
    clean_sheet = BooleanField(default=False)
    penalty_saved = IntegerField(default=0)
    penalty_missed = IntegerField(default=0)

    @property
    def total_score(self):
        total_score = GOAL_POINTS * self.goal + ASSIST_POINTS * self.assist \
            + PENALTY_SAVED_POINTS * self.penalty_saved \
            + PENALTY_MISSED_POINTS * self.penalty_missed

        if self.red_card:
            total_score += RED_CARD_POINTS

        if self.yellow_card:
            total_score += YELLOW_CARD_POINTS

        if self.player.playingRole == "Captain":
            total_score *= 2

        if self.player.playingRole == "GoalKeeper" and self.clean_sheet:
            total_score += CLEAN_SHEET_POINTS

        return total_score

    class Meta:
        unique_together = ['player', 'gameweek']

    def __str__(self):
        return self.player.playerName + " - " + str(self.gameweek)


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
