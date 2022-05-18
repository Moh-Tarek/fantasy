from django.core.management.base import BaseCommand
from Fantasy.models import Fixture, FootballTeam
import os
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        file = open("Fantasy/fixtures/fixtures_2022.json", "r")
        data = file.read()
        file.close()

        json_data = json.loads(data)

        for gameweek, fixtures in json_data.items():
            fixtures_list = []
            for f in fixtures:
                fixtures_list.append(
                    Fixture(
                        gameweek = int(gameweek),
                        team1 = FootballTeam.objects.get(name=f['team1']),
                        team2 = FootballTeam.objects.get(name=f['team2']),
                        date = f['date']
                    )
                )
            Fixture.objects.bulk_create(fixtures_list)
            print(f"{len(fixtures_list)} fixures created in gameweek: {gameweek}")
        