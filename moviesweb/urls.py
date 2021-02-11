"""
URLs for moviesweb application
"""
from django.urls import path

from moviesweb.views import RatingViewList
from . import views

urlpatterns = [
    path('', views.movies, name='movies'),
    path('movies/', views.movies, name='movies'),
    path('details/<identifier>', views.details, name='details'),
    path('details/', views.details, name='details'),
    path('rating/', RatingViewList.as_view(), name='rating'),
]
