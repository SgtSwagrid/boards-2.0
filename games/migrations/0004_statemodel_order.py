# Generated by Django 3.0.7 on 2020-07-28 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20200726_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='statemodel',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]