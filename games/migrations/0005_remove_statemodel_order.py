# Generated by Django 3.0.8 on 2020-07-29 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_statemodel_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statemodel',
            name='order',
        ),
    ]