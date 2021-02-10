from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import TextField


class Movie(models.Model):
    """

    """
    title = models.CharField(max_length=255)  # null=False is deafult so empty title will throw an error
    description = TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """

    """
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewed_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    review_title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])


class Comment(models.Model):
    """

    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
