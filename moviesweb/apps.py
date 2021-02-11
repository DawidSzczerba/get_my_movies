"""Information about the applications that our project includes"""
from django.apps import AppConfig


class MovieswebConfig(AppConfig):
    """Out project contain one app = 'moviesweb'"""
    name: str = 'moviesweb'
