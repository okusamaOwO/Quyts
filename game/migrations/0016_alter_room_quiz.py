# Generated by Django 5.0.2 on 2024-04-18 12:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_room_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='quiz',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='game.quiz'),
        ),
    ]
