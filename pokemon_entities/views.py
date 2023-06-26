import folium
import datetime
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils import timezone

timezone.localtime(timezone.now())
now = datetime.datetime.now()

MOSCOW_CENTER = [55.751244, 37.618423]


def add_pokemon(folium_map, lat, lon, image_url):
    """Добавляет на карту покемонов."""
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    """Отображает всех покемонов на главной странице.

    А также располагает на карте покемонов, которые доступны в данный момент времени.
    """
    pokemons = Pokemon.objects.all()
    map_displayed_pokemons = PokemonEntity.objects.filter(appeared_at__lte=now, disappeared_at__gte=now)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in map_displayed_pokemons:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    """На отдельной странице выводит информацию о каждом покемоне.

    Если они доступны в данный момент, то и их расположение на карте.
    """
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemon = {
        "pokemon_id": pokemon_id,
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": request.build_absolute_uri(requested_pokemon.image.url),
        "previous_evolution": {"pokemon_id": requested_pokemon.previous_evolution_id,
                               "title_ru": requested_pokemon.previous_evolution.title,
                               "img_url": request.build_absolute_uri(requested_pokemon.previous_evolution.image.url)
                               } if requested_pokemon.previous_evolution else None

    }

    try:
        next_evolution = requested_pokemon.pokemon_set.all()[0]
    except IndexError:
        pass
    else:
        pokemon.update({
            "next_evolution": {"pokemon_id": next_evolution.id,
                               "title_ru": next_evolution.title,
                               "img_url": request.build_absolute_uri(
                                   next_evolution.image.url)
                               }
        }
        )

    map_displayed_pokemons = PokemonEntity.objects.filter(pokemon__title=requested_pokemon.title, appeared_at__lte=now,
                                                          disappeared_at__gte=now)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in map_displayed_pokemons:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.image.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
