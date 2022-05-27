var ctx = document.getElementById("PlayersGoalsBarChart");
var players_goals_sorted_all_players = JSON.parse(document.getElementById('players_goals_sorted_all_players').textContent);
var players_goals_sorted_all_scores = JSON.parse(document.getElementById('players_goals_sorted_all_scores').textContent);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: set_data(players_goals_sorted_all_players, players_goals_sorted_all_scores, 'Goals'),
  options: set_options(0, get_max(players_goals_sorted_all_scores))
});

var ctx = document.getElementById("PlayersGoalsGWBarChart");
if(ctx){
    var players_goals_sorted_GW_players = JSON.parse(document.getElementById('players_goals_sorted_GW_players').textContent);
    var players_goals_sorted_GW_scores = JSON.parse(document.getElementById('players_goals_sorted_GW_scores').textContent);
    var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: set_data(players_goals_sorted_GW_players, players_goals_sorted_GW_scores, 'Goals'),
    options: set_options(0, get_max(players_goals_sorted_GW_scores))
    });
}

var ctx = document.getElementById("PlayersAssistsBarChart");
var players_assists_sorted_all_players = JSON.parse(document.getElementById('players_assists_sorted_all_players').textContent);
var players_assists_sorted_all_scores = JSON.parse(document.getElementById('players_assists_sorted_all_scores').textContent);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: set_data(players_assists_sorted_all_players, players_assists_sorted_all_scores, 'Assists'),
  options: set_options(0, get_max(players_assists_sorted_all_scores))
});

var ctx = document.getElementById("PlayersAssistsGWBarChart");
if(ctx){
    var players_assists_sorted_GW_players = JSON.parse(document.getElementById('players_assists_sorted_GW_players').textContent);
    var players_assists_sorted_GW_scores = JSON.parse(document.getElementById('players_assists_sorted_GW_scores').textContent);
    var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: set_data(players_assists_sorted_GW_players, players_assists_sorted_GW_scores, 'Assists'),
    options: set_options(0, get_max(players_assists_sorted_GW_scores))
    });
}

var ctx = document.getElementById("FantasyTeamsBarChart");
var teams_sorted_all_teams = JSON.parse(document.getElementById('teams_sorted_all_teams').textContent);
var teams_sorted_all_scores = JSON.parse(document.getElementById('teams_sorted_all_scores').textContent);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: set_data(teams_sorted_all_teams, teams_sorted_all_scores, 'Points'),
  options: set_options(0, get_max(teams_sorted_all_scores))
});

var ctx = document.getElementById("FantasyTeamsGWBarChart");
if(ctx){
    var teams_sorted_GW_teams = JSON.parse(document.getElementById('teams_sorted_GW_teams').textContent);
    var teams_sorted_GW_scores = JSON.parse(document.getElementById('teams_sorted_GW_scores').textContent);
    var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: set_data(teams_sorted_GW_teams, teams_sorted_GW_scores, 'Points'),
    options: set_options(0, get_max(teams_sorted_GW_scores))
    });
}

var ctx = document.getElementById("FantasyPlayersBarChart");
var players_sorted_all_players = JSON.parse(document.getElementById('players_sorted_all_players').textContent);
var players_sorted_all_scores = JSON.parse(document.getElementById('players_sorted_all_scores').textContent);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: set_data(players_sorted_all_players, players_sorted_all_scores, 'Points'),
  options: set_options(0, get_max(players_sorted_all_scores))
});

var ctx = document.getElementById("FantasyPlayersGWBarChart");
if(ctx){
    var players_sorted_GW_players = JSON.parse(document.getElementById('players_sorted_GW_players').textContent);
    var players_sorted_GW_scores = JSON.parse(document.getElementById('players_sorted_GW_scores').textContent);
    var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: set_data(players_sorted_GW_players, players_sorted_GW_scores, 'Points'),
    options: set_options(0, get_max(players_sorted_GW_scores))
    });
}