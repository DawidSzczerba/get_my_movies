"""
 A model is the single, definitive source of information about your data.
 It contains the essential fields and behaviors of the data you’re storing.
 Generally, each model maps to a single database table.
"""

import django.contrib.auth.models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import TextField, CharField, DateTimeField


class Movie(models.Model):
    """
    Movie model - represent movie in our database
    """
    title: CharField = models.CharField(max_length=255)
    description: TextField = TextField()
    created_at: DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Review model - represents feedback and rating of a movie from our database
    """
    writer = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    reviewed_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    review_title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1),
                                                        MaxValueValidator(10)])


class Comment(models.Model):
    """
    Comment model - represents a comment made by a user of our application about a particular video
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
