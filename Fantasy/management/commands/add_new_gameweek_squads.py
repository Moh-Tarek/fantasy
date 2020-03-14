from django.core.management.base import BaseCommand
from Fantasy.models import FantasySquad, Player
import os

class Command(BaseCommand):
    def is_exist_squad(self, squad):
        squad = FantasySquad.objects.filter(
            team=squad.team,
            gameweek=squad.gameweek
        )
        if squad:
            return True
        return False

    def handle(self, *args, **options):
        # c = 0
        # current_gameweek = int(os.getenv('GAMEWEEK'))
        # previous_gameweek = current_gameweek - 1
        # previous_gameweek_squads = FantasySquad.objects.filter(gameweek=previous_gameweek)
        # current_gameweek_squads = []
        # for squad in previous_gameweek_squads:
        #     squad.pk = None
        #     squad.gameweek = current_gameweek
        #     if not self.is_exist_squad(squad):
        #         c += 1
        #         current_gameweek_squads.append(squad)
        
        # FantasySquad.objects.bulk_create(current_gameweek_squads)
        # print(f'{c} squads created in gameweek {current_gameweek}')
        Player.objects.create(playerName="Test", playingRole="Captain", teamName="test")
        