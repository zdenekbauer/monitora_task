import requests
from bs4 import BeautifulSoup as bs
from crawler.models import Actor, Movie
from django.core.management.base import BaseCommand

CSFD_URL = "https://www.csfd.cz"


def get_soup(path: str):
    response = requests.get(
        f"{CSFD_URL}{path}",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    return bs(response.content, 'html.parser')


class Command(BaseCommand):
    help = 'Scraps data from CSFD top 300 list'

    def handle(self, *args, **options):
        list_soup = get_soup("/zebricky/filmy/nejlepsi/?showMore=1")
        # Box obsahující seznam filmů a z nich linky na ně
        movies = list_soup.find(
            class_="row-300"
        ).find_all(
            class_="film-title-name"
        )

        for movie in movies:
            movie_name = movie.text.strip()
            self.stdout.write(f"Scrapping: {movie_name}")
            movie_soup = get_soup(movie['href'])
            # Rovnou děláme nové objekty, protože při aktualizaci seznamu chceme začínat nad čistou tabulkou
            movie_query = Movie(name=movie_name)
            movie_query.save()

            # Seznam herců
            actors = movie_soup.find("h4", string="Hrají: ").parent.find_all("a")
            for actor in actors:
                # Zahodíme linky co te netýkají herců
                if not actor['href'].startswith('/tvurce'):
                    continue

                actor_name = actor.text.strip()

                try:
                    actor_query = Actor.objects.get(name=actor_name)
                except Actor.DoesNotExist:
                    actor_query = Actor(name=actor_name)
                    actor_query.save()
                actor_query.movies.add(movie_query)

        self.stdout.write(self.style.SUCCESS('Successfully scrapped all data'))
