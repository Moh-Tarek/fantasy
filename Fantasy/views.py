from django.shortcuts import render,redirect
from .models import Player,FantasySquad, FantasyTeam
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SquadSelection,FantasyRegister
from django.views.generic import ListView,DetailView
from datetime import datetime
from django.db.models import Sum
import os
from django.db.models import Q

scores = [
    {
        'userName': 'Mohamed Tarek',
        'fantasyTeamName': 'Ahly',
        'score':'100'
    }
]

def home(request):
    context={'players':Player.objects.all()}
    return render(request,'Fantasy/home.html',context)

def about(request):
    return render(request,'Fantasy/about.html',{'title':'About Fantasy'})

def allPlayers(request):
    players = Player.objects.all()
    playingRoleQuery = request.GET.get('playingRole')
    teamQuery = request.GET.get('teamname')
    if playingRoleQuery!="" and playingRoleQuery is not None and teamQuery!="" and teamQuery is not None:
        if playingRoleQuery != "all" and teamQuery !="all":
            playersRole = players.filter(playingRole = playingRoleQuery)
            playersTeam = players.filter(teamName=teamQuery)
            players = playersRole & playersTeam
        if playingRoleQuery == "all" and teamQuery !="all":
            players = players.filter(teamName=teamQuery)
        if playingRoleQuery != "all" and teamQuery =="all":
            players = players.filter(playingRole = playingRoleQuery)
        if playingRoleQuery == "all" and teamQuery =="all":
            players = Player.objects.all()

    context = {
        'players': players,
        'title':'Show Players'
    }
    return render(request,'Fantasy/all_players.html',context)

@login_required
def register(request):
    if request.method == 'POST':
        form = FantasyRegister(request.POST, my_user=request.user)
        if form.is_valid():
            sub_form = form.save()
            # sub_form.user = request.user
            username = form.cleaned_data.get('FantasyPlayerName')
            messages.success(request, 'Thanks {} for joining us! You can login now!'.format(username))
            return redirect('Fantasy-home')
    else:
        existing_team = FantasyTeam.objects.filter(user=request.user)
        if existing_team.count() == 0:
            form = FantasyRegister()
            return render(request,'Fantasy/register.html',{'form':form})
        return render(request,'Fantasy/register.html',{'team':existing_team[0]})

@login_required
def squadSelectionView(request):
    # 1. get current gameweek number
    gameweek = os.getenv('GAMEWEEK', 1)
    # 2. get the registered team, and redirect to register page if not registered before
    try:
        team = FantasyTeam.objects.get(user=request.user)
    except:
        messages.warning(request, 'You should create a team before selecting a squad')
        return redirect('Fantasy-register')
    # 3. get this gameweek's squad so that the user can edit it, and return empty form if no squad created
    try:
        squad = FantasySquad.objects.get(team=team, gameweek=gameweek)
    except:
        squad = None
    # 4. check request method and continue
    if request.method == 'POST':
        if squad:
            form = SquadSelection(request.POST, team=team, gameweek=gameweek, instance=squad)
        else:
            form = SquadSelection(request.POST, team=team, gameweek=gameweek)
        if form.is_valid():
            sub_form = form.save()
            # sub_form.user = request.user
            messages.success(request, 'Thanks, your Squad has been submitted!')
            # return redirect('Fantasy-allplayers')
            return redirect('Fantasy-squadSelection')
    else:
        if squad:
            form = SquadSelection(instance=squad)
        else:
            form = SquadSelection()
    return render(request,'Fantasy/squad_selection.html', {'form':form, 'gameweek': gameweek})

def fixtures(request):
    return render(request,'Fantasy/fixtures.html',{'title':'Nagwa League Fixtures Season 2020'})
