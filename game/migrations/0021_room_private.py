# Generated by Django 5.0.2 on 2024-04-23 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_alter_question_quiz_alter_room_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='private',
            field=models.BooleanField(default=True),
        ),
    ]
