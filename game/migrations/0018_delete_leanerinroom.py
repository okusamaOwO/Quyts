# Generated by Django 5.0.2 on 2024-04-23 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_alter_room_host'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LeanerInRoom',
        ),
    ]
