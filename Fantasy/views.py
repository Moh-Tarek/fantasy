from django.shortcuts import render, redirect
from .models import Player, FantasySquad, Team
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SquadSelection
from django.views.generic import ListView,DetailView
from django.views import View
from datetime import datetime
from django.db.models import Sum
import os


def home(request):
    context = {'players': Player.objects.all()}
    return render(request, 'Fantasy/home.html', context)

def rules(request):
    return render(request, 'Fantasy/rules.html')

def about(request):
    return render(request, 'Fantasy/about.html', {'title': 'About Fantasy'})


def allPlayers(request):
    players = Player.objects.all()
    playingRoleQuery = request.GET.get('playingRole')
    teamQuery = request.GET.get('teamname')
    if playingRoleQuery != "" and playingRoleQuery is not None and teamQuery != "" and teamQuery is not None:
        if playingRoleQuery != "all" and teamQuery != "all":
            playersRole = players.filter(playingRole=playingRoleQuery)
            playersTeam = players.filter(teamName=teamQuery)
            players = playersRole & playersTeam
        if playingRoleQuery == "all" and teamQuery != "all":
            players = players.filter(teamName=teamQuery)
        if playingRoleQuery != "all" and teamQuery == "all":
            players = players.filter(playingRole=playingRoleQuery)
        if playingRoleQuery == "all" and teamQuery == "all":
            players = Player.objects.all()

    players_sorted = sorted(players, key=lambda x: x.total_player_score, reverse=True)
    context = {
        'players': players_sorted,
        'title': 'Show Players',
        'playingRoleQuery': playingRoleQuery,
        'teamQuery': teamQuery
    }
    return render(request, 'Fantasy/all_players.html', context)


def allTeams(request):
    teams = Team.objects.all()
    teams_sorted = sorted(teams, key=lambda x: x.total_team_score, reverse=True)
    context = {
        'teams': teams_sorted
    }
    return render(request, 'Fantasy/all_teams.html', context)


@login_required
def teamScore(request):
    try:
        team = Team.objects.get(user=request.user)
    except:
        return render(request, 'Fantasy/team_score.html', {'squads': []})

    squads = FantasySquad.objects.filter(team=team)
    return render(request, 'Fantasy/team_score.html', {'squads': squads, 'team': team})


# @login_required
# def register(request):
#     # check existing team
#     try:
#         team = Team.objects.get(user=request.user)
#     except:
#         team = None
#     if request.method == 'POST':
#         if team:
#             form = FantasyRegister(request.POST, my_user=request.user, instance=team)
#         else:
#             form = FantasyRegister(request.POST, my_user=request.user)
#         if form.is_valid():
#             sub_form = form.save()
#             # sub_form.user = request.user
#             username = form.cleaned_data.get('FantasyPlayerName')
#             messages.success(request,
#                              f'Thanks {username} for updating your team details! You can select or update your squad now!')
#             return redirect('Fantasy-squadSelection')
#     else:
#         if team:
#             form = FantasyRegister(instance=team)
#         else:
#             form = FantasyRegister()
#         return render(request, 'Fantasy/register.html', {'form': form})
#         # return render(request,'Fantasy/register.html',{'team':existing_team[0]})


def squadSelectionView(request):
    gameweek = os.getenv('GAMEWEEK', 1)
    
    # 3. get this gameweek's squad so that the user can edit it, and return empty form if no squad created
    try:
        squad = FantasySquad.objects.get(team=request.user, gameweek=gameweek)
    except:
        squad = None
    # 4. check request method and continue
    if request.method == 'POST':
        if squad:
            form = SquadSelection(request.POST, team=request.user, gameweek=gameweek, instance=squad)
        else:
            form = SquadSelection(request.POST, team=request.user, gameweek=gameweek)
        if form.is_valid():
            sub_form = form.save()
            messages.success(request, 'Thanks, your Squad has been submitted!')
            return redirect('Fantasy-squadSelection')
        else:
            messages.warning(request, form.errors)
            return render(request, 'Fantasy/squad_selection.html', {'form': form})
    else:
        if squad:
            form = SquadSelection(instance=squad)
        else:
            form = SquadSelection()
    return render(request, 'Fantasy/squad_selection.html', {'form': form})


def matches(request):
    return render(request, 'Fantasy/matches.html', {'title': 'Nagwa League matches Season 2020'})
