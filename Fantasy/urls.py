from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(login_url='/accounts/google/login')(views.home), name='Fantasy-home'),
    path('gameweek/', login_required(login_url='/accounts/google/login')(views.update_gameweek), name='Fantasy-gameweek'),
    path('rules/', login_required(login_url='/accounts/google/login/')(views.rules), name='Fantasy-rules'),
    path('about/', login_required(login_url='/accounts/google/login/')(views.about), name='Fantasy-about'),
    path('matches/', login_required(login_url='/accounts/google/login/')(views.matches), name='Fantasy-matches'),
    path('allplayers/', login_required(login_url='/accounts/google/login/')(views.allPlayers), name='Fantasy-allplayers'),
    path('teams/', login_required(login_url='/accounts/google/login/')(views.allTeams), name='Fantasy-teams'),
    path('scores/', login_required(login_url='/accounts/google/login/')(views.teamScore), name='Fantasy-score'),
    path('squadselection/', login_required(login_url='/accounts/google/login/')(views.squadSelectionView), name='Fantasy-squadSelection'),
    # path('register/',login_required(login_url='/accounts/google/login/')(views.register), name='Fantasy-register'),
]
