from django.core.management.base import BaseCommand
from Fantasy.models import Fixture, FootballTeam
import os
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        x = Fixture.objects.all().count()
        if x:
            print("There are fixtures already. Please delete the existing fixtures if you need to load them from the beginning.")
            return
            
        file = open("Fantasy/fixtures/fixtures_2022.json", "r")
        data = file.read()
        file.close()

        json_data = json.loads(data)

        

        for gameweek, fixtures in json_data.items():
            fixtures_list = []
            for f in fixtures:
                try: 
                    team1 = FootballTeam.objects.get(name=f['team1'])
                    team1_representation = None
                except: 
                    team1 = None
                    team1_representation = name=f['team1']
                try: 
                    team2 = FootballTeam.objects.get(name=f['team2'])
                    team2_representation = None
                except: 
                    team2 = None
                    team2_representation = name=f['team2']
                stage = f['stage']
                if stage == 'G' and team1.group != team2.group:
                    print(f"Fixture of GW{gameweek} [{team1}] vs [{team2}] not added as it is in group stage, however they are in different groups")
                fixtures_list.append(
                    Fixture(
                        gameweek = int(gameweek),
                        team1 = team1,
                        team1_representation = team1_representation,
                        team2 = team2,
                        team2_representation = team2_representation,
                        stage = stage,
                        date = f['date']
                    )
                )
            Fixture.objects.bulk_create(fixtures_list)
            print(f"{len(fixtures_list)} fixures created in gameweek: {gameweek}")
        