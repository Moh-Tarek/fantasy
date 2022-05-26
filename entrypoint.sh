#! /bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py load_teams_players # if not exist
python manage.py load_groups        # if not exist
python manage.py load_fixtures      # if not exist
python manage.py runserver 0.0.0.0:8000