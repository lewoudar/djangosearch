from django.apps import AppConfig
from watson import search


class StarwarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangosearch.starwars'

    def ready(self):
        search.register(
            self.get_model('Character'),
            store=('name', 'mass', 'height', 'birth_year'),
            fields=(
                'name',
                'skin_color',
                'hair_color',
                'gender',
                'birth_year',
                'movies__title',
                'movies__opening_crawl',
            ),
        )
        search.register(self.get_model('Movie'), store=('release_date',))
