from datetime import date
from typing import Annotated

import httpx
from django.core.management.base import BaseCommand
from pydantic import BaseModel, HttpUrl, Field, BeforeValidator

from djangosearch.starwars.models import Movie, Character


def check_unknown_value(value: str | None) -> str | None:
    if value and value == 'unknown':
        return '0'
    return value.replace(',', '')


class MovieSchema(BaseModel):
    title: str
    release_date: date
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    character_urls: list[HttpUrl] = Field(alias='characters')


class CharacterSchema(BaseModel):
    name: str
    height: Annotated[int, BeforeValidator(check_unknown_value)]
    mass: Annotated[float, BeforeValidator(check_unknown_value)]
    skin_color: str
    hair_color: str
    gender: str
    birth_year: str


class Command(BaseCommand):
    help = 'Add Star Wars characters in the database along with their movies'

    def _fetch_and_save_character(
        self, client: httpx.Client, url: str, movie: Movie, done_urls: dict[str, str], unreachable_urls: set
    ) -> None:
        if url in done_urls:
            character = Character.objects.get(name=done_urls[url])
            movie.characters.add(character)
            return

        try:
            response = client.get(url)
        except httpx.TimeoutException:
            unreachable_urls.add(url)
            return

        if response.status_code >= 400:
            unreachable_urls.add(url)
            self.stdout.write(f'{url} is unreachable')
            return

        character_model = CharacterSchema(**response.json())
        character = Character.objects.create(**character_model.model_dump())
        movie.characters.add(character)
        done_urls[url] = character_model.name
        self.stdout.write(f'Character {character_model.name} saved')

    def handle(self, *args, **options):
        done_urls: dict[str, str] = {}
        unreachable_urls: set[str] = set()
        with httpx.Client(base_url='https://swapi.dev/api', timeout=10) as client:
            self.stdout.write('Processing movies')
            response = client.get('/films/')

            for movie_data in response.json()['results']:
                movie_model = MovieSchema(**movie_data)
                movie = Movie.objects.create(**movie_model.model_dump(exclude={'character_urls'}))
                for url in movie_model.character_urls:
                    url = str(url)  # we cast HttpUrl to str
                    if url in unreachable_urls:
                        continue
                    self._fetch_and_save_character(client, url, movie, done_urls, unreachable_urls)

        self.stdout.write(self.style.SUCCESS('Processing terminated'))
