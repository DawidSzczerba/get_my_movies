"""
URLs for moviesweb application
"""
from typing import List, Union

from django.urls import path
from django.urls.resolvers import URLResolver, URLPattern

from moviesweb.views import RatingViewList
from . import views

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('', views.movies, name='movies'),
    path('movies/', views.movies, name='movies'),
    path('details/<identifier>', views.details, name='details'),
    path('details/', views.details, name='details'),
    path('rating/', RatingViewList.as_view(), name='rating'),
]
