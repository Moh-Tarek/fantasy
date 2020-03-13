# Generated by Django 3.0.4 on 2020-03-13 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Fantasy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fantasyteam',
            name='nagwaID',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fantasyteam',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
