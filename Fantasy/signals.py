from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import GameweekSetting, FantasySquad

def is_exist_squad(squad):
    squad = FantasySquad.objects.filter(
        team=squad.team,
        gameweek=squad.gameweek
    )
    if squad:
        return True
    return False

def create_squads(current_gameweek, previous_gameweek_squads):
    c = 0
    current_gameweek_squads = []
    for squad in previous_gameweek_squads:
        squad.pk = None
        squad.gameweek = current_gameweek
        if not is_exist_squad(squad):
            c += 1
            current_gameweek_squads.append(squad)
    
    FantasySquad.objects.bulk_create(current_gameweek_squads)
    print(f'{c} squads created in gameweek {current_gameweek}')

@receiver(post_save, sender=GameweekSetting)
def add_new_gameweek_squads(sender, instance, created, **kwargs):
    if not created:
        current_gameweek = instance.active_gameweek
        previous_gameweek = current_gameweek - 1
        if previous_gameweek > 0:
            previous_gameweek_squads = FantasySquad.objects.filter(gameweek=previous_gameweek)
            create_squads(current_gameweek, previous_gameweek_squads)