# Generated by Django 4.2.7 on 2024-03-19 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_alter_chessroom_board_alter_chessroom_moves'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuessRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomId', models.CharField(max_length=6)),
                ('number1', models.CharField(blank=True, max_length=3, null=True)),
                ('number2', models.CharField(blank=True, max_length=3, null=True)),
                ('guess1', models.CharField(blank=True, max_length=10000, null=True)),
                ('guess2', models.CharField(blank=True, max_length=10000, null=True)),
                ('player1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2', to=settings.AUTH_USER_MODEL)),
                ('viewers', models.ManyToManyField(blank=True, null=True, related_name='viewers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
