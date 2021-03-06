"""Serializers allow complex data such as querysets and model instances to be converted to native
   Python datatypes that can then be easily rendered into JSON, XML or other content types.
   Serializers also provide deserialization, allowing parsed data to be converted back into complex
   types, after first validating the incoming dataSerializers for moviesweb applications"""
from typing import Type

import django.contrib.auth.models
from rest_framework import serializers

from moviesweb.models import Movie, Comment, Review


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User model serializer
    """

    class Meta:
        model: Type = django.contrib.auth.models.User
        fields = ['username', 'email']


class MovieSerializer(serializers.ModelSerializer):
    """
    Movie model serializer
    """
    class Meta:
        model: Type[Movie] = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment model serializer
    """
    class Meta:
        model: Type[Comment] = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review model serializer
    """
    class Meta:
        model: Type[Review] = Review
        fields = '__all__'
