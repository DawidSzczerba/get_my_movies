from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework import routers

from moviesweb.views import RatingViewList
from . import views

urlpatterns = [
    path('', views.movies, name='movies'),
    path('movies/', views.movies, name='movies'),
    path('details/<identifier>', views.details, name='details'),
    path('details/', views.details, name='details'),
    path('rating/', RatingViewList.as_view(), name='rating'),
]
