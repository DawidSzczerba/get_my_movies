from django.contrib import admin

# Register your models here.
from moviesweb.models import Movie, Review, Comment

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Comment)
