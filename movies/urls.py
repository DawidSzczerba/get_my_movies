"""moviesweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import List, Union

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.urls.resolvers import URLResolver, URLPattern
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from moviesweb.views import UserViewSet

from moviesweb import views

router: DefaultRouter = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'my_movies', views.MovieViewSet, basename='movie')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'reviews', views.ReviewViewSet, basename='reviews')

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('signup/', views.signup, name='signup'),
    path("logout/", views.logout_request, name="logout"),
    path("", include(router.urls)),
    path("", include('moviesweb.urls')),
]
