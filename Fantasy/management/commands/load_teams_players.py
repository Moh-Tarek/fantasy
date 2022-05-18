from django.core.management.base import BaseCommand
from Fantasy.models import FootballTeam, Player
import os
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        file = open("Fantasy/fixtures/teams_players_2022.json", "r")
        data = file.read()
        file.close()

        json_data = json.loads(data)

        for team_name, players in json_data.items():
            t = FootballTeam.objects.create(name=team_name)
            players_list = []
            for playing_role, name in players.items():
                if isinstance(name, str):
                    name = [name]
                for i in name:
                    players_list.append(
                        Player(
                            playingRole = playing_role,
                            playerName = i,
                            team = t
                        )
                    )
            Player.objects.bulk_create(players_list)
            print(f"{len(players_list)} players created in team: {team_name}")
        