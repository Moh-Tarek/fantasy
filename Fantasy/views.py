from django.forms import DateField
from django.shortcuts import render, redirect
from .models import Fixture, FootballTeam, Group, Player, FantasySquad, Team, GameweekSetting, Score
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from .forms import GameweekSettingForm, LimitedScoreForm, ScoreForm, SquadSelection, FixtureWithdrawForm
from . import utils


def home(request):
    try:
        gameweek = GameweekSetting.objects.last().active_gameweek
    except:
        gameweek = 1
    previous_gameweek = gameweek - 1

    teams = Team.objects.all()
    teams_with_squads = teams.filter(squads__isnull=False).distinct()
    
    teams_selection_count = 5 if teams.count() >= 5 else teams.count()
    teams_sorted_all = sorted(teams, key=lambda x: x.total_team_score, reverse=True)[:teams_selection_count]
    teams_sorted_all_teams = []
    teams_sorted_all_scores = []
    for t in teams_sorted_all:
        teams_sorted_all_teams.append([t.first_name, t.last_name])
        teams_sorted_all_scores.append(t.total_team_score)

    teams_sorted_GW = sorted(teams, key=lambda x: x.last_gameweek_team_score or 0, reverse=True)[:teams_selection_count]
    teams_sorted_GW_teams = []
    teams_sorted_GW_scores = []
    for t in teams_sorted_GW:
        teams_sorted_GW_teams.append([t.first_name, t.last_name])
        teams_sorted_GW_scores.append(t.last_gameweek_team_score or 0)
    
    matches = Fixture.objects.all()
    matches_GW = matches.filter(gameweek=gameweek)
    matches_completed = [ i for i in matches if i.is_finished ]

    groups = Group.objects.all()
    f_teams = FootballTeam.objects.all()
    
    f_players = Player.objects.all()

    plyrs_sorted = sorted(f_players, key=lambda x: x.total_player_score, reverse=True)
    plyrs_sorted_by_GW = sorted(f_players, key=lambda x: x.last_gameweek_player_score, reverse=True)

    dream_team_all = utils.get_dream_team(plyrs_sorted)
    dream_team_GW = utils.get_dream_team(plyrs_sorted_by_GW)

    players_selection_count = 5 if f_players.count() >= 5 else f_players.count()
    players_sorted_all = plyrs_sorted[:players_selection_count]
    players_sorted_all_players = []
    players_sorted_all_scores = []
    for p in players_sorted_all:
        players_sorted_all_players.append(p.playerName.split(" "))
        players_sorted_all_scores.append(p.total_player_score)

    players_sorted_GW = plyrs_sorted_by_GW[:players_selection_count]
    players_sorted_GW_players = []
    players_sorted_GW_scores = []
    for p in players_sorted_GW:
        players_sorted_GW_players.append(p.playerName.split(" "))
        players_sorted_GW_scores.append(p.last_gameweek_player_score)

    players_goals_sorted_all = sorted(f_players, key=lambda x: x.player_scores.get_goals_sum(), reverse=True)[:players_selection_count]
    players_goals_sorted_all_players = []
    players_goals_sorted_all_scores = []
    for p in players_goals_sorted_all:
        players_goals_sorted_all_players.append(p.playerName.split(" "))
        players_goals_sorted_all_scores.append(p.player_scores.get_goals_sum())

    players_goals_sorted_GW = sorted(f_players, key=lambda x: x.last_gameweek_player_score_objs.get_goals_sum(), reverse=True)[:players_selection_count]
    players_goals_sorted_GW_players = []
    players_goals_sorted_GW_scores = []
    for p in players_goals_sorted_GW:
        players_goals_sorted_GW_players.append(p.playerName.split(" "))
        players_goals_sorted_GW_scores.append(p.last_gameweek_player_score_objs.get_goals_sum())

    players_assists_sorted_all = sorted(f_players, key=lambda x: x.player_scores.get_assists_sum(), reverse=True)[:players_selection_count]
    players_assists_sorted_all_players = []
    players_assists_sorted_all_scores = []
    for p in players_assists_sorted_all:
        players_assists_sorted_all_players.append(p.playerName.split(" "))
        players_assists_sorted_all_scores.append(p.player_scores.get_assists_sum())

    players_assists_sorted_GW = sorted(f_players, key=lambda x: x.last_gameweek_player_score_objs.get_assists_sum(), reverse=True)[:players_selection_count]
    players_assists_sorted_GW_players = []
    players_assists_sorted_GW_scores = []
    for p in players_assists_sorted_GW:
        players_assists_sorted_GW_players.append(p.playerName.split(" "))
        players_assists_sorted_GW_scores.append(p.last_gameweek_player_score_objs.get_assists_sum())

    # most owned players every gameweek
    most_owned_players = {}
    all_squads = FantasySquad.objects
    for g in range(1, gameweek):
        # get counts 
        squads = all_squads.filter(gameweek=g)
        c = list(squads.values(p=F('captainSelected__playerName')).annotate(c=Count('captainSelected')))
        gk = list(squads.values(p=F('goalKeeperSelected__playerName')).annotate(c=Count('goalKeeperSelected')))
        p1 = list(squads.values(p=F('player1Selected__playerName')).annotate(c=Count('player1Selected')))
        p2 = list(squads.values(p=F('player2Selected__playerName')).annotate(c=Count('player2Selected')))
        p3 = list(squads.values(p=F('player3Selected__playerName')).annotate(c=Count('player3Selected')))
        p4 = list(squads.values(p=F('player4Selected__playerName')).annotate(c=Count('player4Selected')))
        p5 = list(squads.values(p=F('player5Selected__playerName')).annotate(c=Count('player5Selected')))
        squads_players = c + gk + p1 + p2 + p3 + p4 + p5
        # concat with player id and get it selection count
        squads_players_sum = {}
        for i in squads_players:
            p = i['p']
            if p not in squads_players_sum.keys():
                squads_players_sum[p] = 0
            squads_players_sum[p] += i['c']
        # convert count into ratio
        squads_count = squads.count()
        squads_players_ratio = []
        for k, v in squads_players_sum.items():
            squads_players_ratio.append((k, round(v/squads_count*100, 2)))
        squads_players_ratio.sort(key = lambda x: x[1], reverse=True)

        most_owned_players[g] = squads_players_ratio

    most_owned_players_all = {}
    max = 3
    if len(most_owned_players.keys()) <= 3:
        max = 5
    for gw, value in most_owned_players.items():
        most_owned_players_GW_players = []
        most_owned_players_GW_perc = []
        index = 0
        for plyr, perc in value:
            most_owned_players_GW_players.append(plyr.split(" "))
            most_owned_players_GW_perc.append(perc)
            index += 1
            if index == max:
                break
        most_owned_players_all[gw] = [most_owned_players_GW_players, most_owned_players_GW_perc]

    max = 5
    most_owned_players_GW = []
    if previous_gameweek in most_owned_players.keys():
        most_owned_players_GW = most_owned_players[previous_gameweek]
    most_owned_players_GW_players = []
    most_owned_players_GW_perc = []
    index = 0
    for plyr, perc in most_owned_players_GW:
        most_owned_players_GW_players.append(plyr.split(" "))
        most_owned_players_GW_perc.append(perc)
        index += 1
        if index == max:
            break

    context = {
        'teams': teams.count,
        'teams_with_squads': teams_with_squads.count,
        'teams_sorted_all_teams': teams_sorted_all_teams,
        'teams_sorted_all_scores': teams_sorted_all_scores,
        'teams_sorted_GW_teams': teams_sorted_GW_teams,
        'teams_sorted_GW_scores': teams_sorted_GW_scores,
        'dream_team_all': dream_team_all,
        'dream_team_GW': dream_team_GW,
        'players_sorted_all_players': players_sorted_all_players,
        'players_sorted_all_scores': players_sorted_all_scores,
        'players_sorted_GW_players': players_sorted_GW_players,
        'players_sorted_GW_scores': players_sorted_GW_scores,
        'players_goals_sorted_all_players': players_goals_sorted_all_players,
        'players_goals_sorted_all_scores': players_goals_sorted_all_scores,
        'players_goals_sorted_GW_players': players_goals_sorted_GW_players,
        'players_goals_sorted_GW_scores': players_goals_sorted_GW_scores,
        'players_assists_sorted_all_players': players_assists_sorted_all_players,
        'players_assists_sorted_all_scores': players_assists_sorted_all_scores,
        'players_assists_sorted_GW_players': players_assists_sorted_GW_players,
        'players_assists_sorted_GW_scores': players_assists_sorted_GW_scores,
        'matches': matches.count,
        'matches_GW': matches_GW.count,
        'matches_completed': len(matches_completed),
        'f_teams': f_teams.count,
        'groups': groups.count,
        'f_players': f_players.count,
        'most_owned_players': most_owned_players,
        'most_owned_players_all': most_owned_players_all,
        'most_owned_players_GW_players': most_owned_players_GW_players,
        'most_owned_players_GW_perc': most_owned_players_GW_perc
    }
    
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

def league_rules(request):
    return render(request, 'Fantasy/league_rules.html')

def about(request):
    return render(request, 'Fantasy/about.html', {'title': 'About Fantasy'})

def update_match_stats(request, id):
    fixture = Fixture.objects.get(pk=id)
    gameweek = GameweekSetting.objects.last().active_gameweek
    previous_gameweek = gameweek - 1
    if (not (request.user.is_staff or request.user.is_superuser)) or ((not request.user.is_superuser) and fixture.gameweek != previous_gameweek):
        # all staff users can update the previous gameweek's fixtures stats only. Superusers can update any gameweek's fixtures stats.
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
        # save withdrawn team with fixture and if so, return without saving the score
        fw = FixtureWithdrawForm(request.POST, instance=fixture)
        if fw.is_valid():
            updated_fixture = fw.save()
            if updated_fixture.withdrawn_team:
                w_team = updated_fixture.withdrawn_team
                # remove withdrawn team scores
                if w_team == team1:
                    team1_fixture_scores.delete()
                elif w_team == team2:
                    team2_fixture_scores.delete()
                # use limitedScoreForm for the other team scores (it includes played points only)
                LimitedScoreFormSet = modelformset_factory(Score, extra=0, form=LimitedScoreForm)
                if w_team == team1:
                    team_fixture_scores_formset = LimitedScoreFormSet(request.POST, queryset=team2_fixture_scores, prefix='team' + str(team2.pk))
                elif w_team == team2:
                    team_fixture_scores_formset = LimitedScoreFormSet(request.POST, queryset=team1_fixture_scores, prefix='team' + str(team1.pk))   
                if team_fixture_scores_formset.is_valid():
                    for form in team_fixture_scores_formset:
                        if form.is_valid():
                            updated_score_obj = form.save()
                            # add clean sheet to the goalkeeper if he played
                            if updated_score_obj.player.playingRole == 'GoalKeeper': # and updated_score_obj.played == True: (check scoring algorithm)
                                updated_score_obj.clean_sheet = True
                                updated_score_obj.save()
                        print(form.errors)
                else:
                    print(team_fixture_scores_formset.errors)
                return redirect('Fantasy-matches')
        else:
            print(fw.errors)
        ################# withrawal part ended #######################
        team1_fixture_scores_formset = ScoreFormSet(request.POST, queryset=team1_fixture_scores, prefix='team' + str(team1.pk))
        team2_fixture_scores_formset = ScoreFormSet(request.POST, queryset=team2_fixture_scores, prefix='team' + str(team2.pk))   
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
        ## withdraw form that has the option to select one of the fixture teams as withdrawn team
        fw = FixtureWithdrawForm(instance=fixture)
        ## create formsets for all the scores objects
        team1_fixture_scores_formset = ScoreFormSet(queryset=team1_fixture_scores, prefix='team' + str(team1.pk))
        team2_fixture_scores_formset = ScoreFormSet(queryset=team2_fixture_scores, prefix='team' + str(team2.pk))
    
    return render(request, 'Fantasy/update_match_stats.html', {
        'fixture': fixture, 
        'fw': fw,
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

    squads = FantasySquad.objects.filter(team=team).exclude(gameweek=active_gameweek)

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


def squadPointsView(request):
    try:
        gameweek = GameweekSetting.objects.last().active_gameweek
    except:
        gameweek = 1
    previous_gameweek = gameweek-1
    
    ## get this gameweek's squad so that the user can edit it, and return empty squad if no squad created
    try:
        squad = FantasySquad.objects.get(team=request.user, gameweek=previous_gameweek)
    except:
        squad = None

    fixtures = Fixture.objects.filter(gameweek=previous_gameweek)
    fixtures_grouped = utils.group_fixtures_by_stage(fixtures)
    return render(request, 'Fantasy/squad_points_view.html', {'squad': squad, 'fixtures_grouped': fixtures_grouped})

def squadSelectionView(request):
    try:
        gameweek = GameweekSetting.objects.last().active_gameweek
    except:
        gameweek = 1
    
    ## get this gameweek's squad so that the user can edit it, and return empty squad if no squad created
    try:
        squad = FantasySquad.objects.get(team=request.user, gameweek=gameweek)
    except:
        squad = None

    fixtures = Fixture.objects.filter(gameweek=gameweek)
    fixtures_grouped = utils.group_fixtures_by_stage(fixtures)

    players_data = {}
    players = Player.objects.all()
    teams = FootballTeam.objects.all()
    teams_against = {}
    for t in teams:
        t_h, t_a = t.fixtures
        t_h = [i.team2.short_name for i in t_h.filter(gameweek=gameweek)]
        t_a = [i.team1.short_name for i in t_a.filter(gameweek=gameweek)]
        teams_against[t.short_name] = t_h + t_a
    for p in players:
        p_team = p.team.short_name
        color = p.team.color
        p_against = teams_against[p_team]
        players_data[p.id] = {
            'name': p.playerName,
            'team': p_team,
            'color': color,
            'vs': ",".join(p_against)
        }
    # print(players_data)

    ## check request method and continue
    if request.method == 'POST':
        if squad:
            form = SquadSelection(request.POST, team=request.user, gameweek=gameweek, instance=squad)
        else:
            form = SquadSelection(request.POST, team=request.user, gameweek=gameweek)
        if form.is_valid():
            print("form saved")
            sub_form = form.save()
            messages.success(request, 'Thanks, your Squad has been submitted!')
            return redirect('Fantasy-squadSelection')
        else:
            print("form issue")
            print(form.errors)
            messages.warning(request, form.errors)
            return render(request, 'Fantasy/squad_selection.html', {'form': form, 'squad': form.instance, 'players_data': players_data, 'fixtures_grouped': fixtures_grouped})
    else:
        if squad:
            form = SquadSelection(instance=squad)
        else:
            form = SquadSelection()
    
    return render(request, 'Fantasy/squad_selection.html', {'form': form, 'squad': form.instance if form.instance.pk else None, 'players_data': players_data, 'fixtures_grouped': fixtures_grouped})


def matches(request):
    fixtures = Fixture.objects.all()
    fixtures_grouped = utils.group_fixtures_by_stage(fixtures)
    return render(request, 'Fantasy/matches.html', {'fixtures_grouped': fixtures_grouped})


def groups(request):
    # 1. get each group stats
    data = {}
    groups = Group.objects.all()
    for g in groups:
        group_fixtures = Fixture.objects.filter(stage="G", team1__group=g)
        data[g.name] = utils.get_group_stats(g, group_fixtures)

    # 2. rank each group teams depending on stats
    ranked_data = {}
    for g, teams in data.items():
        # flatten each group stats dict to list by adding team name beside its stats
        # from: { 'team_1: {'W': 2,...}, ... }
        # to:   [ {'team': 'team_1', 'W': 2,...}, ... ]
        teams_stats = []
        for t, stats in teams.items():
            stats['team'] = t
            teams_stats.append(stats)
        # sort
        teams_stats = utils.sort_by(
            teams_stats, 
            [
                {'value': ('P', True)},
                {'win_versus': ('W_vs', 'team')},
                {'value': ('GD', True)}, 
                {'value': ('GS', True)},
                # {'value': ('team', False)}
            ]
        )
        # teams_stats.sort(key=operator.itemgetter('team'))      
        # teams_stats.sort(key=operator.itemgetter('GC'))  
        # teams_stats.sort(key=operator.itemgetter('GS'), reverse=True)  
        # teams_stats.sort(key=operator.itemgetter('GD'), reverse=True)    
        # teams_stats.sort(key=operator.itemgetter('P'), reverse=True)
        ranked_data[g] = teams_stats

    return render(request, 'Fantasy/groups.html', {'ranked_data': ranked_data})

def matchesVideos(request):
    fixtures = Fixture.objects.all()
    played_fixtures_grouped_by_stage_and_gw = utils.group_fixtures_by_stage_and_gw(fixtures, match_urls_only=True)

    query_gw = request.GET.get('gw')
    if query_gw:
        query_gw = int(query_gw)
    query_match_id = request.GET.get('id', '')

    return render(request, 'Fantasy/matches-videos.html', {
        'played_fixtures_grouped_by_stage_and_gw': played_fixtures_grouped_by_stage_and_gw,
        'gw': query_gw,
        'match_id': query_match_id
    })

