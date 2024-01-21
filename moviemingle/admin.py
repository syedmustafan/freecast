from django.contrib import admin
from .models import Source, Movie, Show, Season, Episode

admin.site.register(Source)
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Season)
admin.site.register(Episode)