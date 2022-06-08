from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Fantasy.models import FantasySquad, GameweekSetting, Player, Team
import random

class Command(BaseCommand):

    def handle(self, *args, **options):
        # create random squads for every GW
        all_c = list(Player.objects.filter(playingRole="Captain"))
        all_g = list(Player.objects.filter(playingRole="GoalKeeper"))
        all_p = list(Player.objects.filter(playingRole="Player"))
        squads = []
        teams = Team.objects.all()
        gw = GameweekSetting.objects.last().active_gameweek
        for i in range(1, gw):
            print(f"GW{i}:")
            index = 0
            for t in teams:
                s = FantasySquad.objects.filter(team=t, gameweek=i)
                if not s:
                    index += 1
                    FantasySquad.objects.create(
                        team=t, 
                        gameweek=i,
                        captainSelected=random.choice(all_c),
                        goalKeeperSelected=random.choice(all_g),
                        player1Selected=random.choice(all_p),
                        player2Selected=random.choice(all_p),
                        player3Selected=random.choice(all_p),
                        player4Selected=random.choice(all_p),
                        player5Selected=random.choice(all_p),
                    )
            print(f"{index} squads have been created.")
            
        