## Before Deployment:
- Update the football teams and their players in: Fantasy/fixtures/teams_players.json
- Update the matches and their gameweeks and dates in: Fantasy/fixtures/fixtures_2022.json

## After Deployment, run:
- python manage.py load_teams_players.py
- python manage.py load_fixtures.py

## Each gameweek:
- Update Gameweek Settings to your new active gameweek and its deadline
