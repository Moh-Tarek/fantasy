# Generated by Django 3.0.4 on 2020-03-08 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Fantasy', '0005_fantasysquad_captinselected'),
    ]

    operations = [
        migrations.AddField(
            model_name='fantasysquad',
            name='goalKeeperSelected',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='GK', to='Fantasy.Player'),
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='player2Selected',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='P2', to='Fantasy.Player'),
        ),
        migrations.AddField(
            model_name='fantasysquad',
            name='player3Selected',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='P3', to='Fantasy.Player'),
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
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='P1', to='Fantasy.Player'),
        ),
    ]