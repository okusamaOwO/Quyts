# Generated by Django 5.0.2 on 2024-05-03 10:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0004_cards_setname'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cards',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='cards',
            name='subject',
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcards.subject')),
            ],
        ),
        migrations.AlterField(
            model_name='cards',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcards.tag'),
        ),
    ]
