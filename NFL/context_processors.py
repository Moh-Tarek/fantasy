from ast import Not
from Fantasy.models import GameweekSetting
from generic.models import Alarm, Notifications

def gameweek_variables(request):
    try:
        gameweek_setting = GameweekSetting.objects.first()
        gameweek = gameweek_setting.active_gameweek
        gameweek_deadline = gameweek_setting.gameweek_deadline
    except:
        gameweek = 1
        gameweek_deadline = "(To be updated)"
    previous_gameweek = gameweek - 1
    return {
        "gameweek" :gameweek,
        "previous_gameweek": previous_gameweek,
        "gameweek_deadline": gameweek_deadline
    }

def alarm_notification_variables(request):
    alarms = Alarm.objects.all()
    notifications = Notifications.objects.all()
    return {
        'alarms': alarms,
        'notifications': notifications
    }