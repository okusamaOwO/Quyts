# Generated by Django 5.0.2 on 2024-04-18 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_leanerinroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.quiz'),
        ),
    ]
