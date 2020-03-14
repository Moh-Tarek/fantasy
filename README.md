## After deploy, run:

- python manage.py loaddata players.json  (for players data)
- python manage.py loaddata users.json         (for users data)
- python manage.py loaddata teams.json         (to create a team for each user)

- python manage.py loaddata squads.json        (for gameweek 1 squads)
- python manage.py loaddata scores.json        (for gameweek 1 players scores)

## Each gameweek:

- edit .env and update the variables: GAMEWEEK & GAMEWEEK_DEADLINE
- run: python manage.py add_new_gameweek_squads
