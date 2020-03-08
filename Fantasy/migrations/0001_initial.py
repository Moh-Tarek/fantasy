# Generated by Django 2.1.3 on 2020-03-08 15:02

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
            name='FantasySquad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastRoundScore', models.IntegerField()),
                ('overallScore', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FantasyTeam',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('FantasyPlayerName', models.CharField(max_length=100)),
                ('FantasyTeamName', models.CharField(max_length=100)),
                ('lastRoundScore', models.IntegerField()),
                ('overallScore', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('playerName', models.CharField(max_length=100)),
                ('image', models.ImageField(default='defaultplayer.jpg', upload_to='profile_pics')),
                ('teamName', models.CharField(max_length=100)),
                ('playingRole', models.CharField(choices=[('Captin', 'Captin'), ('GoalKeeper', 'GoalKeeper'), ('Player', 'Player')], max_length=100)),
                ('lastRoundScore', models.IntegerField()),
                ('overallScore', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='captinSelected',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='C', to='Fantasy.Player'),
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='goalKeeperSelected',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GK', to='Fantasy.Player'),
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='player2Selected',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='P2', to='Fantasy.Player'),
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='player3Selected',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='P3', to='Fantasy.Player'),
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='player4Selected',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='P4', to='Fantasy.Player'),
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='player5Selected',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='P5', to='Fantasy.Player'),
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='players1Selected',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='P1', to='Fantasy.Player'),
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
