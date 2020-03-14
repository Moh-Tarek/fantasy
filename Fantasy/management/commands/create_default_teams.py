from django.core.management.base import BaseCommand
from Fantasy.models import FantasyTeam
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        teams_to_be_created = []
        all_users = User.objects.all()
        for u in all_users:
            team = FantasyTeam.objects.filter(user=u)
            if not team:
                teams_to_be_created.append(
                    FantasyTeam(
                        user = u,
                        FantasyPlayerName = u.username,
                        FantasyTeamName = u.username + ' Team'
                    )
                )
        FantasyTeam.objects.bulk_create(teams_to_be_created)
        x = len(teams_to_be_created)
        if x == 0:
            print("All users have teams already! No new teams created.")
        if x == 1:
            print("1 team created successfully!")
        else:
            print(f"{x} teams created successfully!")