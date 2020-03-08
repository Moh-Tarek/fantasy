from django.shortcuts import render,redirect
from .models import Player,FantasySquad
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SquadSelection
from django.views.generic import ListView,DetailView
from datetime import datetime
from django.db.models import Sum

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
    playingRoleQuery = request.GET.get('category')
    context = {'players':Player.objects.all()}
    if playingRoleQuery!="":
        context = {'players':Player.objects.all().filter(playingRole=playingRoleQuery)}

    return render(request,'Fantasy/all_players.html',context,{'title':'All Players'})

@login_required
def squadSelectionView(request):
    if request.method == 'POST':
        form = SquadSelection(request.POST)
        if form.is_valid():
            sub_form = form.save()
            sub_form.user = request.user
            messages.success(request, 'Thanks, your Squad has been submitted!')
            return redirect('Fantasy-allplayers')
    else:
        form = SquadSelection()
    return render(request,'Fantasy/squad_selection.html', {'form':form})
