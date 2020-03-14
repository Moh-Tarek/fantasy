import os


def gameweek_variables(request):
    gameweek = int(os.getenv('GAMEWEEK', 1))
    gameweek_deadline = os.getenv('GAMEWEEK_DEADLINE')
    return {"gameweek" :gameweek, "gameweek_deadline": gameweek_deadline}