from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField(blank=True, default=None)
    lon = models.FloatField(blank=True, default=None)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=None)
