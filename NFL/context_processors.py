from Fantasy.models import GameweekSetting


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