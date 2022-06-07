var ctx = document.getElementById("PlayersSelectionBarChart");
if(ctx){
  var most_owned_players_all = JSON.parse(document.getElementById('most_owned_players_all').textContent);
  var x_data = Object.keys(most_owned_players_all)
  var y_values = Object.values(most_owned_players_all)
  var y_data = [];var y_data_names = []
  // x_data.forEach(_ => {y_data.push([]);y_data_names.push([])});
  var x = 0
  y_values.forEach(element => {
    var plyrs = element[0]
    var percs = element[1]
    if(x == 0){percs.forEach(_ => {y_data.push([]);y_data_names.push([])});}
    x = x + 1
    var index = 0
    percs.forEach(e =>{y_data[index].push(e);index = index + 1})
    index = 0
    plyrs.forEach(e =>{y_data_names[index].push(e);index = index + 1})
  })
  var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: set_multi_data(x_data, y_data, y_data_names, '%'),
  options: set_options(0, 100, 'Gameweek', 'Owned By %', 'GW', y_data_names)
  });
}

var ctx = document.getElementById("PlayersSelectionGWBarChart");
if(ctx){
    var most_owned_players_GW_players = JSON.parse(document.getElementById('most_owned_players_GW_players').textContent);
    var most_owned_players_GW_perc = JSON.parse(document.getElementById('most_owned_players_GW_perc').textContent);
    var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: set_data(most_owned_players_GW_players, most_owned_players_GW_perc, '%'),
    options: set_options(0, get_max(most_owned_players_GW_perc), 'Players', 'Owned By %')
    });
}

var ctx = document.getElementById("PlayersGoalsBarChart");
var players_goals_sorted_all_players = JSON.parse(document.getElementById('players_goals_sorted_all_players').textContent);
var players_goals_sorted_all_scores = JSON.parse(document.getElementById('players_goals_sorted_all_scores').textContent);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: set_data(players_goals_sorted_all_players, players_goals_sorted_all_scores, 'Goals'),
  options: set_options(0, get_max(players_goals_sorted_all_scores), 'Players', 'Goals')
});

var ctx = document.getElementById("PlayersGoalsGWBarChart");
if(ctx){
    var players_goals_sorted_GW_players = JSON.parse(document.getElementById('players_goals_sorted_GW_players').textContent);
    var players_goals_sorted_GW_scores = JSON.parse(document.getElementById('players_goals_sorted_GW_scores').textContent);
    var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: set_data(players_goals_sorted_GW_players, players_goals_sorted_GW_scores, 'Goals'),
    options: set_options(0, get_max(players_goals_sorted_GW_scores), 'Players', 'Goals')
    });
}

var ctx = document.getElementById("PlayersAssistsBarChart");
var players_assists_sorted_all_players = JSON.parse(document.getElementById('players_assists_sorted_all_players').textContent);
var players_assists_sorted_all_scores = JSON.parse(document.getElementById('players_assists_sorted_all_scores').textContent);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: set_data(players_assists_sorted_all_players, players_assists_sorted_all_scores, 'Assists'),
  options: set_options(0, get_max(players_assists_sorted_all_scores), 'Players', 'Assists')
});

var ctx = document.getElementById("PlayersAssistsGWBarChart");
if(ctx){
    var players_assists_sorted_GW_players = JSON.parse(document.getElementById('players_assists_sorted_GW_players').textContent);
    var players_assists_sorted_GW_scores = JSON.parse(document.getElementById('players_assists_sorted_GW_scores').textContent);
    var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: set_data(players_assists_sorted_GW_players, players_assists_sorted_GW_scores, 'Assists'),
    options: set_options(0, get_max(players_assists_sorted_GW_scores), 'Players', 'Assists')
    });
}

var ctx = document.getElementById("FantasyTeamsBarChart");
var teams_sorted_all_teams = JSON.parse(document.getElementById('teams_sorted_all_teams').textContent);
var teams_sorted_all_scores = JSON.parse(document.getElementById('teams_sorted_all_scores').textContent);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: set_data(teams_sorted_all_teams, teams_sorted_all_scores, 'Points'),
  options: set_options(0, get_max(teams_sorted_all_scores), 'Fantasy Teams', 'Total Score')
});

var ctx = document.getElementById("FantasyTeamsGWBarChart");
if(ctx){
    var teams_sorted_GW_teams = JSON.parse(document.getElementById('teams_sorted_GW_teams').textContent);
    var teams_sorted_GW_scores = JSON.parse(document.getElementById('teams_sorted_GW_scores').textContent);
    var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: set_data(teams_sorted_GW_teams, teams_sorted_GW_scores, 'Points'),
    options: set_options(0, get_max(teams_sorted_GW_scores), 'Fantasy Teams', 'GW Score')
    });
}

var ctx = document.getElementById("FantasyPlayersBarChart");
var players_sorted_all_players = JSON.parse(document.getElementById('players_sorted_all_players').textContent);
var players_sorted_all_scores = JSON.parse(document.getElementById('players_sorted_all_scores').textContent);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: set_data(players_sorted_all_players, players_sorted_all_scores, 'Points'),
  options: set_options(0, get_max(players_sorted_all_scores), 'Players', 'Total Score')
});

var ctx = document.getElementById("FantasyPlayersGWBarChart");
if(ctx){
    var players_sorted_GW_players = JSON.parse(document.getElementById('players_sorted_GW_players').textContent);
    var players_sorted_GW_scores = JSON.parse(document.getElementById('players_sorted_GW_scores').textContent);
    var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: set_data(players_sorted_GW_players, players_sorted_GW_scores, 'Points'),
    options: set_options(0, get_max(players_sorted_GW_scores), 'Players', 'GW Score')
    });
}