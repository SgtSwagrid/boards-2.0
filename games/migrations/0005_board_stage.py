# Generated by Django 3.0.7 on 2020-06-24 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_board_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='stage',
            field=models.IntegerField(default=0),
        ),
    ]
