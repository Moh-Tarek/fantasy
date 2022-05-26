from django.core.management.base import BaseCommand
from Fantasy.models import Group, FootballTeam
import os
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        x = Group.objects.all().count()
        if x:
            print("There are groups already. Please delete the existing groups if you need to load them from the beginning.")
            return

        file = open("Fantasy/fixtures/groups_2022.json", "r")
        data = file.read()
        file.close()

        json_data = json.loads(data)

        for group_name, teams in json_data.items():
            g = Group.objects.create(name=group_name)
            i = 0
            for t in teams:
                t = FootballTeam.objects.get(name=t)
                t.group = g
                t.save()
                i += 1
            print(f"{i} teams added in group: {group_name}")
        