from django.shortcuts import render, redirect
from .models import Fixture, Player, FantasySquad, Team, GameweekSetting, Score
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import GameweekSettingForm, ScoreForm, SquadSelection


def home(request):
    context = {'players': Player.objects.all()}
    return render(request, 'Fantasy/home.html', context)

def update_gameweek(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('Fantasy-matches')
    try:
        gameweek_setting = GameweekSetting.objects.last()
    except:
        gameweek_setting = None

    if request.method == 'POST':
        if gameweek_setting:
            form = GameweekSettingForm(request.POST, instance=gameweek_setting)
        else:
            form = GameweekSettingForm(request.POST)
        if form.is_valid():
            sub_form = form.save()
            return redirect('Fantasy-matches')
        else:
            messages.warning(request, form.errors)
            return render(request, 'Fantasy/gameweek_settings.html', {'form': form})
    else:
        if gameweek_setting:
            form = GameweekSettingForm(instance=gameweek_setting)
        else:
            form = GameweekSettingForm()
    return render(request, 'Fantasy/gameweek_settings.html', {'form': form})

def rules(request):
    return render(request, 'Fantasy/rules.html')

def about(request):
    return render(request, 'Fantasy/about.html', {'title': 'About Fantasy'})

def update_match_stats(request, id):
    fixture = Fixture.objects.get(pk=id)
    gameweek = GameweekSetting.objects.last().active_gameweek
    if (not (request.user.is_staff or request.user.is_superuser)) or ((not request.user.is_superuser) and fixture.gameweek != gameweek):
        # all staff users can update the active gameweek's fixtures stats only. Superusers can update any gameweek's fixtures stats.
        return redirect('Fantasy-matches')

    f_scores = fixture.scores
    team1 = fixture.team1
    team2 = fixture.team2

    ## create empty score object for players with the corresponding fixture in not exist
    for p in fixture.players:
        player_fixture_score = f_scores.filter(player=p)
        if not player_fixture_score:
            player_fixture_score = Score.objects.create(player=p, fixture=fixture)
    
    from django.forms import modelformset_factory
    ScoreFormSet = modelformset_factory(Score, extra=0, form=ScoreForm)
    team1_fixture_scores = f_scores.filter(player__team=team1)
    team2_fixture_scores = f_scores.filter(player__team=team2)

    if request.method == 'POST':
        team1_fixture_scores_formset = ScoreFormSet(request.POST, queryset=team1_fixture_scores, prefix='team1')
        team2_fixture_scores_formset = ScoreFormSet(request.POST, queryset=team2_fixture_scores, prefix='team2')    
        for formset in [team1_fixture_scores_formset, team2_fixture_scores_formset]:
            if formset.is_valid():
                for form in formset:
                    if form.is_valid():
                        form.save()
                    print(form.errors)
            else:
                print(formset.errors)
        return redirect('Fantasy-matches')
    else:
        team1_fixture_scores_formset = ScoreFormSet(queryset=team1_fixture_scores, prefix='team1')
        team2_fixture_scores_formset = ScoreFormSet(queryset=team2_fixture_scores, prefix='team2')
    
    return render(request, 'Fantasy/update_match_stats.html', {
        'fixture': fixture, 
        't1_formset': team1_fixture_scores_formset,
        't2_formset': team2_fixture_scores_formset
    })
    

def allPlayers(request):
    players = Player.objects.all()
    playingRoleQuery = request.GET.get('playingRole')
    teamQuery = request.GET.get('teamname')
    if playingRoleQuery != "" and playingRoleQuery is not None and teamQuery != "" and teamQuery is not None:
        if playingRoleQuery != "all" and teamQuery != "all":
            playersRole = players.filter(playingRole=playingRoleQuery)
            playersTeam = players.filter(team__name=teamQuery)
            players = playersRole & playersTeam
        if playingRoleQuery == "all" and teamQuery != "all":
            players = players.filter(team__name=teamQuery)
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
def teamScore(request, id=None):
    active_gameweek = GameweekSetting.objects.last().active_gameweek
    try:
        if not id:
            team = Team.objects.get(username=request.user)
        else:
            team = Team.objects.get(pk=id)
    except:
        return render(request, 'Fantasy/team_score.html', {'squads': []})

    squads = FantasySquad.objects.filter(team=team)
    if id != request.user.id:
        # hide the current gameweek squads from other users
        squads = squads.exclude(gameweek=active_gameweek)
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
    try:
        gameweek = GameweekSetting.objects.last().active_gameweek
    except:
        gameweek = 1
    
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
    fixtures = Fixture.objects.all()
    return render(request, 'Fantasy/matches.html', {'fixtures': fixtures})
