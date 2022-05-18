from django.contrib import admin
from .models import Fixture, FootballTeam, GameweekSetting, Player, Team, FantasySquad, Score

admin.site.register(GameweekSetting)
admin.site.register(FootballTeam)
admin.site.register(Fixture)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(FantasySquad)
admin.site.register(Score)
