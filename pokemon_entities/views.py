import folium
import json
import datetime

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils import timezone

timezone.localtime(timezone.now())
now = datetime.datetime.now()

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemons_entities = PokemonEntity.objects.filter(appeared_at__lte=now, disappeared_at__gte=now)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            if pokemon_entity.pokemon.image else None
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else None,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)

    if requested_pokemon:
        pokemon = {
            "pokemon_id": pokemon_id,
            "title_ru": requested_pokemon.title,
            "title_en": requested_pokemon.title_en,
            "title_jp": requested_pokemon.title_jp,
            "description": requested_pokemon.description,
            "img_url": request.build_absolute_uri(requested_pokemon.image.url) \
                if requested_pokemon.image else None,
            "previous_evolution": {"pokemon_id": requested_pokemon.previous_evolution_id,
                                   "title_ru": requested_pokemon.previous_evolution.title,
                                   "img_url": request.build_absolute_uri(requested_pokemon.previous_evolution.image.url)
                                   } if requested_pokemon.previous_evolution else None,

        }
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entities = PokemonEntity.objects.filter(pokemon__title=requested_pokemon.title, appeared_at__lte=now,
                                                    disappeared_at__gte=now)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            if pokemon_entity.pokemon.image else None
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
