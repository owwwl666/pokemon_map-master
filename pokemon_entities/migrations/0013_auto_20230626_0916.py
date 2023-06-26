# Generated by Django 3.1.14 on 2023-06-25 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0012_pokemonentity_previous_evolution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemonentity',
            name='previous_evolution',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon'),
        ),
    ]