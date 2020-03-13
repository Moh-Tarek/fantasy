# Generated by Django 3.0.4 on 2020-03-13 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerName', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(default='defaultplayer.jpg', upload_to='profile_pics')),
                ('teamName', models.CharField(max_length=100)),
                ('playingRole', models.CharField(choices=[('Captin', 'Captin'), ('GoalKeeper', 'GoalKeeper'), ('Player', 'Player')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FantasyTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FantasyPlayerName', models.CharField(max_length=100)),
                ('FantasyTeamName', models.CharField(max_length=100)),
                ('nagwaID', models.IntegerField(null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FantasySquad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameweek', models.IntegerField()),
                ('captinSelected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='C', to='Fantasy.Player')),
                ('goalKeeperSelected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='GK', to='Fantasy.Player')),
                ('player1Selected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='P1', to='Fantasy.Player')),
                ('player2Selected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='P2', to='Fantasy.Player')),
                ('player3Selected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='P3', to='Fantasy.Player')),
                ('player4Selected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='P4', to='Fantasy.Player')),
                ('player5Selected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='P5', to='Fantasy.Player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='squads', to='Fantasy.FantasyTeam')),
            ],
        ),
    ]