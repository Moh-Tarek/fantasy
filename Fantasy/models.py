from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class FantasyTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FantasyPlayerName = models.CharField(max_length=100)
    FantasyTeamName = models.CharField(max_length=100)
    nagwaID = models.IntegerField(null=True, blank=True)
    # lastRoundScore = models.IntegerField(null=True)
    # overallScore = models.IntegerField(null=True)


class Player(models.Model):
    playerName = models.CharField(max_length=100, unique=True)
    image = models.ImageField(default='defaultplayer.jpg', upload_to='profile_pics')
    teamName = models.CharField(max_length=100)
    playingRoleChoices = (
        ('Captain', 'Captain'),
        ('GoalKeeper', 'GoalKeeper'),
        ('Player', 'Player'),
    )
    playingRole = models.CharField(max_length=100, choices=playingRoleChoices)
    # lastRoundScore = models.IntegerField()
    # overallScore = models.IntegerField()

    def __str__(self):
        return self.playerName


class FantasySquad(models.Model):
    team = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE, related_name="squads")
    captainSelected = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='C')
    goalKeeperSelected = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='GK')
    player1Selected = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='P1')
    player2Selected = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='P2')
    player3Selected = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='P3')
    player4Selected = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='P4')
    player5Selected = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='P5')
    gameweek = models.IntegerField()
    # lastRoundScore = models.IntegerField()
    # overallScore = models.IntegerField()