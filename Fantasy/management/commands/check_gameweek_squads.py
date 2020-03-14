from django.core.management.base import BaseCommand
from Fantasy.models import FantasySquad
import os
from Fantasy.forms import SquadSelection

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
        current_gameweek = int(os.getenv('GAMEWEEK'))
        current_gameweek_squads = FantasySquad.objects.filter(gameweek=current_gameweek)
        for squad in current_gameweek_squads:
            form = SquadSelection({
                'team':squad.team,
                'gameweek':squad.gameweek,
                'captainSelected':squad.captainSelected,
                'goalKeeperSelected':squad.goalKeeperSelected,
                'player1Selected':squad.player1Selected,
                'player2Selected':squad.player2Selected,
                'player3Selected':squad.player3Selected,
                'player4Selected':squad.player4Selected,
                'player5Selected':squad.player5Selected
            })
            if form.is_valid():
                continue
            else:
                print(squad.team.user)
                print(form.errors)

        