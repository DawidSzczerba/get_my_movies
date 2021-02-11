"""
Class with all views in moviesweb application
"""
from configparser import ConfigParser
from typing import Type, Any, Dict, List, Union, Optional

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import django.contrib.auth.models
from django.db.models import Avg
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

import tmdbsimple as tmdb  # type: ignore

from requests import HTTPError

from rest_framework import viewsets, status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from tmdbsimple import Movies

from moviesweb.forms import SignUpForm
from moviesweb.models import Comment, Movie, Review
from moviesweb.serializers import UserSerializer, CommentSerializer, MovieSerializer, \
    ReviewSerializer

config = ConfigParser()
config.read('moviesweb/config.cfg')
tmdb.API_KEY = config['tmdb']['API_KEY']


class UserViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    A simple UserViewSet - extends viewsets.ModelViewSet from rest_framework
    for User model
    """
    queryset: BaseManager = django.contrib.auth.models.User.objects.all()
    serializer_class: Type = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
        A simple UserViewSet - extends viewsets.ModelViewSet from rest_framework
        for User model
        Allows you to filter movie by title
        Additionally overrides the create method of the ModelViewSet,
        in order to properly create the view object in the rest api, i.e. in case the user doesn't
        provide a movie description, the description will be searched in The Movies Database
        Library  API and provide the title from the movie that was returned first for the title.
    """
    queryset = Movie.objects.all().order_by('-created_at')
    serializer_class = MovieSerializer

    def get_queryset(self) -> QuerySet:
        queryset = Movie.objects.all()
        print(queryset)
        title = self.request.query_params.get("title", None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)
        return queryset

    def create(self, request, *args, **kwargs) -> Response:

        try:
            results_from_tmdb = tmdb.Search().movie(query=request.data['title'])['results']
        except HTTPError as http_error:
            raise ParseError(
                detail="Malformed Request. A movie with this title does not exist or the movie"
                       " you specified is empty ") from http_error

        overview = request.data['description']
        if not overview:
            overview = results_from_tmdb[0]['overview'] if results_from_tmdb else ""

        serializer = self.get_serializer(
            data={
                'title': request.data['title'],
                'description': overview
            })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
        A simple CommentViewSet - extends viewsets.ModelViewSet from rest_framework
        for Comment model
        Overriding the get_queryset method allows you to allows you to filter comments by movie id
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self) -> QuerySet:
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is not None:
            queryset = queryset.filter(movie__id=movie_id)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
        A simple ReviewViewSet - extends viewsets.ModelViewSet from rest_framework
        for Review model
        Overriding the get_queryset method allows you to allows you to filter reviews
        by reviewed_movie_id or writer_id
    """
    serializer_class: Type[ReviewSerializer] = ReviewSerializer
    queryset: BaseManager[Any] = Review.objects.all().order_by('-rating')

    def get_queryset(self) -> QuerySet:
        queryset: BaseManager[Any] = Review.objects.all()
        movie_id: Optional[Any] = self.request.query_params.get('reviewed_movie_id', None)
        if movie_id is not None:
            queryset = queryset.filter(reviewed_movie__id=movie_id)

        writer_id: Optional[Any] = self.request.query_params.get('writer_id', None)
        if writer_id is not None:
            queryset = queryset.filter(writer__id=writer_id)

        return queryset


class RatingViewList(LoginRequiredMixin, ListView):  # pylint: disable=too-many-ancestors
    """
    This view displays the ranking of movies based on user ratings.
    RatingViewList view connected with Review model, usage the get_querset method
    allows determine the list of objects that user can display.
    """
    model: Type[Review] = Review
    template_name: str = "moviesweb/rating.html"
    context_object_name: str = "movies"

    def get_queryset(self) -> QuerySet:
        return Movie.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')


def movies(request: HttpRequest) -> HttpResponse:
    """
        This is a function-based view to get the movie list for a particular search query, using
        tmdbsimple library to calls tmbd api.
    :param request: request from the front-end API call
    :return: render method at the movie.html endpoint with the required search results.
    """
    query = str(request.GET.get(key='query', default='The Dark Knight'))
    if query != '':
        search_result = tmdb.Search().movie(query=query)['results'][0:9]
        frontend: Dict[str, Union[Union[List[Any], bool], Any]] = {
            "search_result": sorted(search_result, key=lambda x: x['popularity'], reverse=True),
            "has_result": search_result != []
        }
    else:
        frontend = {
            "search_result": [],
            "has_result": False
        }
    return render(request=request, template_name="moviesweb/movie.html", context=frontend)


@login_required(login_url='/login')
def details(request: HttpRequest, identifier: int = 0) -> HttpResponse:
    """
        This is a function-based view to get the movie details for a particular list click,
        using tmdbsimple library to calls tmbd api.
    :param request: request from the front-end API call
    :param identifier: id of the movie clicked on
    :return: render method at the details.html endpoint with
        the required movie details.
    """
    movie: Movies = tmdb.Movies(id=identifier)
    trailers: List[Any] = list(filter(lambda v: v['type'] == 'Trailer', movie.videos()['results']))
    frontend: Dict[str, Union[List[Any], Any]] = {
        "info": movie.info(),
        "year": movie.info()['release_date'][:4],
        "production": movie.info()['production_companies'][:2],
        "cast": movie.credits()['cast'][:10],
        "crew": movie.credits()['crew'][:5],
        "trailers": trailers,
    }
    return render(request=request, template_name="moviesweb/details.html", context=frontend)


def signup(request: HttpRequest) -> HttpResponse:
    """
    Simple function based view to serve singup functionality
    :param request: request from the front-end API call
    :return: render method at the signup.html endpoint with
        the page to singup
    """
    if request.method == 'POST':
        form: SignUpForm = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(to='/movies')
    else:
        form = SignUpForm()
    return render(request=request, template_name='registration/signup.html', context={'form': form})


def logout_request(request: HttpRequest) -> HttpResponse:
    """
    Simple function based view to serve logout functionality
    :param request: request from the front-end API call
    :return: render method at the logout.html endpoint with
        the page to logout
    """
    logout(request)
    messages.info(request=request, message="Logged out successfully!")
    return redirect(to="/movies")
