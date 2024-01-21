import json

import requests
from celery import shared_task
from django.utils import timezone

from moviemingle.models import Movie, Source, Show


@shared_task
def import_shows():
    """
        Celery task to import TV shows from a JSON API and update the database.

        The JSON data is fetched from a specified URL and processed to update or
        create Show objects in the database. For each show, related Source objects
        are also created or updated.

        Raises:
            Exception: If an error occurs during the import process.
    """
    json_url = 'https://channelsapi.s3.amazonaws.com/media/test/shows.json'

    try:
        response = requests.get(json_url)
        data = json.loads(response.text)
        for show_data in data:
            show, created = Show.objects.update_or_create(
                id=show_data['id'],
                defaults={
                    'title': show_data['name'],
                    'description': show_data['description'],
                    'image': show_data['image'],
                    'release_date': show_data['first_aired'],
                    'imdb_rating': show_data.get('imdb_rating', None),
                    'kinopoisk_rating': show_data.get('kinopoisk_rating', None),
                }
            )

            # Create or update Sources for the Show
            for source_data in show_data['modes']['web_sources']['subscriptions']:
                source, _ = Source.objects.get_or_create(
                    id=source_data['id'],
                    defaults={
                        'url': source_data['name'],
                    }
                )
                show.sources.add(source)

            print(f'Successfully imported shows: {show.title}')

    except Exception as e:
        print(f'Error importing shows: {str(e)}')


@shared_task
def import_movies():
    """
       Celery task to import movies from a JSON API and update the database.

       The JSON data is fetched from a specified URL and processed to update or
       create Movie objects in the database. For each movie, related Source objects
       are also created or updated.

       Raises:
           Exception: If an error occurs during the import process.
    """
    json_url = 'https://channelsapi.s3.amazonaws.com/media/test/movies.json'

    try:
        response = requests.get(json_url)
        data = json.loads(response.text)

        for movie_data in data:
            movie, created = Movie.objects.update_or_create(
                id=movie_data['id'],
                defaults={
                    'title': movie_data['name'],
                    'description': movie_data['description'],
                    'image': movie_data['image'],
                    'release_date': f"{movie_data['release_year']}-01-01",
                    'imdb_rating': movie_data.get('imdb_rating', None),
                    'kinopoisk_rating': movie_data.get('kinopoisk_rating', None),
                }
            )

            for source_data in movie_data['modes']['web_sources']['subscriptions']:
                source, _ = Source.objects.get_or_create(
                    id=source_data['id'],
                    defaults={
                        'url': source_data['name'],
                    }
                )
                movie.sources.add(source)

            print(f'Successfully imported movie: {movie.title}')

    except Exception as e:
        print(f'Error importing movies: {str(e)}')


@shared_task
def test_sources():
    # Get all movies and shows with their sources
    movies = Movie.objects.all()
    shows = Show.objects.all()

    # Test sources for movies
    for movie in movies:
        movie.test_and_update_movie_sources()

    # Test sources for shows
    for show in shows:
        show.test_and_update_show_sources()
