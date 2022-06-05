# Generated by Django 3.0.4 on 2022-06-05 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generic', '0002_auto_20220604_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alarm',
            old_name='alarm_content',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='alarm',
            old_name='alarm_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='alarm',
            old_name='alarm_header',
            new_name='header',
        ),
        migrations.RenameField(
            model_name='notifications',
            old_name='notifications_content',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='notifications',
            old_name='notifications_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='notifications',
            old_name='notifications_header',
            new_name='header',
        ),
        migrations.AddField(
            model_name='alarm',
            name='icon_tag',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='alarm',
            name='url',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='notifications',
            name='icon_tag',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='notifications',
            name='url',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]