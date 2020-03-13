from django.shortcuts import render,redirect
from .models import Player,FantasySquad, FantasyRegister
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SquadSelection,FantasyRegister
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
    playingRoleQuery = request.GET.get('category', None)
    context = {'players':Player.objects.all()}
    if not playingRoleQuery is None:
        context = {'players':Player.objects.all().filter(playingRole=playingRoleQuery)}
    context['title'] = 'All Players'
    return render(request,'Fantasy/all_players.html',context)

@login_required
def register(request):
    if request.method == 'POST':
        form = FantasyRegister(request.POST, my_user=request.user)
        if form.is_valid():
            sub_form = form.save()
            sub_form.user = request.user
            username = form.cleaned_data.get('FantasyPlayerName')
            messages.success(request, 'Thanks {} for joining us! You can login now!'.format(username))
            return redirect('Fantasy-home')
    else:
        form = FantasyRegister()
    return render(request,'Fantasy/register.html',{'form':form})

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
