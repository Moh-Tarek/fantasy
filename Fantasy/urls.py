from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(login_url='/accounts/google/login')(views.home), name='Fantasy-home'),
    path('gameweek/', login_required(login_url='/accounts/google/login')(views.update_gameweek), name='Fantasy-gameweek'),
    path('rules/', login_required(login_url='/accounts/google/login/')(views.rules), name='Fantasy-rules'),
    path('league_rules/', login_required(login_url='/accounts/google/login/')(views.league_rules), name='Fantasy-league-rules'),
    path('about/', login_required(login_url='/accounts/google/login/')(views.about), name='Fantasy-about'),
    path('matches/', login_required(login_url='/accounts/google/login/')(views.matches), name='Fantasy-matches'),
    path('groups/', login_required(login_url='/accounts/google/login/')(views.groups), name='Fantasy-groups'),
    path('updatestats/<int:id>/', login_required(login_url='/accounts/google/login')(views.update_match_stats), name='Fantasy-update_match_stats'),
    path('allplayers/', login_required(login_url='/accounts/google/login/')(views.allPlayers), name='Fantasy-allplayers'),
    path('teams/', login_required(login_url='/accounts/google/login/')(views.allTeams), name='Fantasy-teams'),
    path('scores/', login_required(login_url='/accounts/google/login/')(views.teamScore), name='Fantasy-score'),
    path('scores/<int:id>/', login_required(login_url='/accounts/google/login/')(views.teamScore), name='Fantasy-score-others'),
    path('squadselection/', login_required(login_url='/accounts/google/login/')(views.squadSelectionView), name='Fantasy-squadSelection'),
    path('points/', login_required(login_url='/accounts/google/login/')(views.squadPointsView), name='Fantasy-squad'),
    # path('register/',login_required(login_url='/accounts/google/login/')(views.register), name='Fantasy-register'),
]
