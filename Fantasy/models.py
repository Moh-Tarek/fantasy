from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class FantasyTeam(models.Model):
    id = models.AutoField(primary_key=True)
    FantasyPlayerName = models.CharField(max_length=100)
    FantasyTeamName = models.CharField(max_length=100)
    lastRoundScore = models.IntegerField()
    overallScore = models.IntegerField()


class Player(models.Model):
    index = models.AutoField(primary_key=True)
    playerName = models.CharField(max_length=100)
    image = models.ImageField(default='defaultplayer.jpg', upload_to='profile_pics')
    teamName = models.CharField(max_length=100)
    playingRoleChoices = (
        ('Captin', 'Captin'),
        ('GoalKeeper', 'GoalKeeper'),
        ('Player', 'Player'),
    )
    playingRole = models.CharField(max_length=100, choices=playingRoleChoices)
    lastRoundScore = models.IntegerField()
    overallScore = models.IntegerField()

    def __str__(self):
        return self.playerName


class FantasySquad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    captinSelected = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='C', null=True, blank=True)
    goalKeeperSelected = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='GK', null=True, blank=True)
    players1Selected = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='P1', null=True, blank=True)
    player2Selected = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='P2', null=True, blank=True)
    player3Selected = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='P3', null=True, blank=True)
    player4Selected = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='P4', null=True)
    player5Selected = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='P5', null=True)
    lastRoundScore = models.IntegerField()
    overallScore = models.IntegerField()
