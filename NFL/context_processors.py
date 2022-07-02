from ast import Not
from Fantasy.models import GameweekSetting
from generic.models import Alarm, Notifications

def gameweek_variables(request):
    try:
        gameweek_setting = GameweekSetting.objects.first()
        gameweek = gameweek_setting.active_gameweek
        gameweek_deadline = gameweek_setting.gameweek_deadline
        max_players_same_team = gameweek_setting.max_players_same_team
    except:
        gameweek = 1
        gameweek_deadline = "(To be updated)"
        max_players_same_team = 2
    previous_gameweek = gameweek - 1
    return {
        "gameweek" :gameweek,
        "previous_gameweek": previous_gameweek,
        "gameweek_deadline": gameweek_deadline,
        "max_players_same_team": max_players_same_team
    }

def alarm_notification_variables(request):
    alarms = Alarm.objects.all()
    notifications = Notifications.objects.all()
    return {
        'alarms': alarms,
        'notifications': notifications
    }