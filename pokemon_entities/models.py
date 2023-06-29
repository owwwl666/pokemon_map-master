from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Название на английском")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="Название на японском")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='images', verbose_name="Картинка")
    previous_evolution = models.ForeignKey("Pokemon", on_delete=models.SET_NULL, blank=True, null=True,
                                           verbose_name="Из кого эволюционировал", related_name='next_evolutions')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    timezone.localtime(timezone.now())
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон",
                                related_name='pokemon_entities')
    lat = models.FloatField(verbose_name="Местоположение (Широта)")
    lon = models.FloatField(verbose_name="Местоположение (Долгота)")
    appeared_at = models.DateTimeField(verbose_name="Время появления на карте")
    disappeared_at = models.DateTimeField(verbose_name="Время исчезновения с карты")
    level = models.IntegerField(blank=True, null=True, verbose_name="Уровень")
    health = models.IntegerField(blank=True, null=True, verbose_name="Здоровье")
    strength = models.IntegerField(blank=True, null=True, verbose_name="Сила")
    defence = models.IntegerField(blank=True, null=True, verbose_name="Защита")
    stamina = models.IntegerField(blank=True, null=True, verbose_name="Выносливость")

    def __str__(self):
        return self.pokemon.title
