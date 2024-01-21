from django.db import models

from moviemingle.utils import test_source


class Source(models.Model):
    url = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.url


class Movie(models.Model):
    title = models.CharField(max_length=255)
    imdb_rating = models.FloatField(null=True, blank=True)
    kinopoisk_rating = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    release_date = models.DateField()
    sources = models.ManyToManyField(Source)

    def __str__(self):
        return self.title

    def test_and_update_movie_sources(self):
        # Test each source
        for source in self.sources.all():
            is_source_valid = test_source(source.url)

            # Mark source as inactive if it's not valid
            source.is_active = is_source_valid
            source.save()


class Show(models.Model):
    title = models.CharField(max_length=255)
    imdb_rating = models.FloatField(null=True, blank=True)
    kinopoisk_rating = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    release_date = models.DateField()
    sources = models.ManyToManyField(Source)

    def __str__(self):
        return self.title

    def test_and_update_show_sources(self):
        # Test each source
        for source in self.sources.all():
            is_source_valid = test_source(source.url)

            # Mark source as inactive if it's not valid
            source.is_active = is_source_valid
            source.save()



class Season(models.Model):
    number = models.PositiveIntegerField()
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.show.title} Season {self.number}'


class Episode(models.Model):
    number = models.PositiveIntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    sources = models.ManyToManyField(Source)

    def __str__(self):
        return f'{self.season.show.title} Season {self.season.number} Episode {self.number}'
