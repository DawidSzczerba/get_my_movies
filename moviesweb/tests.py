"""
Testing of moviesweb application url's and url's of the whole get-my-movies project. Tests check if
the url's are using the correct views and if a connection to the page is possible and if the status
of the connection is appropriate: the most common should be status = 200
"""
from django.contrib.auth.views import LoginView
from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework.response import Response

from rest_framework.test import APIClient, APITestCase

import tmdbsimple as tmdb  # type: ignore

from moviesweb.views import movies, signup, logout_request


class URLTest(TestCase):
    """
    Testing of moviesweb application url's and url's of the whole get-my-movies project. Tests check
    if the url's are using the correct views and if a connection to the page is possible and if
    the status of the connection is appropriate: the most common should be status = 200
    """

    def test_movies_url(self) -> None:
        """
        Tests movies url - connected with view movies
        :rtype: object
        """
        url = reverse('movies')
        self.assertEqual(resolve(url).func, movies)

        client = Client()
        response = client.get(reverse('movies'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self) -> None:
        """
        Tests login url - connected with login view
        :rtype: object
        """
        url = reverse('login')
        self.assertEqual(resolve(url).func.__name__, LoginView.__name__)

        client = Client()
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self) -> None:
        """
        Tests signup url - connected with signup view
        :rtype: object
        """
        url = reverse('signup')
        self.assertEqual(resolve(url).func.__name__, signup.__name__)

        client = Client()
        response = client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self) -> None:
        """
        Tests logout url - connected with logout view
        :rtype: object
        """
        url = reverse('logout')
        self.assertEqual(resolve(url).func.__name__, logout_request.__name__)

        client = Client()
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class MovieTest(APITestCase):
    """
    This class contains tests for the endpoint /my_movies
    """
    client = APIClient()

    def test_post_movie_with_own_description(self) -> None:
        """
        Test if it is possible to use the post method and add a video to the database with
        a description written by the user
        :rtype: object
        """
        response = self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'MOJ TESTOWY OPIS'
        })
        self.assertEqual(response.data['title'], 'cat')
        self.assertEqual(response.data['description'], 'MOJ TESTOWY OPIS')
        self.assertEqual(response.status_code, 201)

    def test_post_movie_with_description_tmdb(self) -> None:
        """
        Test if it is possible to use the post method and add with it to the database a movie with
        the description taken from The Movies Database Library API using the tmdbsimple library
        :rtype: object
        """
        title = 'Joker'
        response = self.client.post('/my_movies/', data={
            'title': title, 'description': ''
        })

        description_from_tmdb = tmdb.Search().movie(query=title)['results'][0]['overview']

        self.assertEqual(response.data['title'], 'Joker')
        self.assertEqual(response.data['description'], description_from_tmdb)
        self.assertEqual(response.status_code, 201)

    def test_post_movie_no_title(self) -> None:
        """
        Checks if we get a corresponding error when trying to upload a movie without a title -
        this should not be possible and the status code should be 400
        :rtype: object
        """
        response = self.client.post('/my_movies/', data={
            'title': '', 'description': ''
        })
        self.assertEqual(response.status_code, 400)

    def test_get_movies(self) -> None:
        """
        Test get method for movies
        :rtype: object
        """
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ala ma kota',
        })
        self.client.post('/my_movies/', data={
            'title': 'django', 'description': 'ala ma kota',
        })
        response = self.client.get('/my_movies/')
        self.assertEqual(len(response.data), 2)


class CommentTest(APITestCase):
    """
    This class contains tests for the endpoint /comments
    """
    client: APIClient = APIClient()

    def test_post_comment(self) -> None:
        """
        Checks if it is possible to add a comment and if we get the right responses from the
        database
        :rtype: object
        """
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ala ma kota',
        })
        response: Response = self.client.post('/comments/', data={
            'movie': '1', 'comment_text': 'ala ma psa'
        })
        self.assertEqual(response.data['movie'], 1)
        self.assertEqual(response.data['comment_text'], 'ala ma psa')

    def test_get_comments(self) -> None:
        """
        Checks if it is possible to use get method for comments and checks if we get right responses
        :rtype: object
        """
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ala ma kota',
        })
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'ala ma kota'})
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'ala ma psa'})
        response = self.client.get('/comments/')
        self.assertEqual(len(response.data), 2)

    def test_get_filtered_comments(self) -> None:
        """
        Checks if it is possible to get comments for a given movie - test of get method
        :rtype: object
        """
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ads',
        })
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'ala ma kota'})
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'ala ma psa'})
        response = self.client.get('/comments/?movie_id=1')
        self.assertEqual(len(response.data), 2)
        for i in response.data:
            self.assertEqual(i['movie'], 1)


class ReviewTest(APITestCase):
    """
    This class contains tests for the endpoint /reviews
    """
    client = APIClient()

    def test_post_review(self) -> None:
        """
        Checks if it is possible to add a review and if we get the right responses from the
        database
        :rtype: object
        """
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ads',
        })

        self.client.post('/users/', data={
            'username': 'sddsf', 'email': 'dawid100298@o2.pl',
        })

        response: Response = self.client.post('/reviews/', data={
            'review_title': 'Batman', 'content': 'ala ma kota', 'rating': '10', 'writer': '1',
            'reviewed_movie': '1',
        })

        self.assertEqual(response.data['review_title'], 'Batman')
        self.assertEqual(response.data['content'], 'ala ma kota')
        self.assertEqual(response.data['rating'], 10)
        self.assertEqual(response.data['writer'], 1)
        self.assertEqual(response.data['reviewed_movie'], 1)

    def test_get_review(self) -> None:
        """
        Checks if it is possible to use get method for reviews and if we get the right
        responses from the database
        :rtype: object
        """
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ads',
        })

        self.client.post('/users/', data={
            'username': 'sddsf', 'email': 'dawid100298@o2.pl',
        })

        self.client.post('/reviews/', data={
            'review_title': 'Batman', 'content': 'ala ma kota', 'rating': '10', 'writer': '1',
            'reviewed_movie': '1',
        })
        self.client.post('/reviews/', data={
            'review_title': 'Batmann', 'content': 'ala ma kotan', 'rating': '10', 'writer': '1',
            'reviewed_movie': '1',
        })

        response = self.client.get('/reviews/')

        self.assertEqual(len(response.data), 2)

    def test_get_filtered_comments(self) -> None:
        """
        Checks if it is possible to get reviews for a given movie - test of get method
        :rtype: object
        """
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ads',
        })

        self.client.post('/users/', data={
            'username': 'sddsf', 'email': 'dawid100298@o2.pl',
        })

        self.client.post('/reviews/', data={
            'review_title': 'Batman', 'content': 'ala ma kota', 'rating': '10', 'writer': '1',
            'reviewed_movie': '1',
        })
        self.client.post('/reviews/', data={
            'review_title': 'Batmann', 'content': 'ala ma kotan', 'rating': '10', 'writer': '1',
            'reviewed_movie': '1',
        })

        response = self.client.get('/reviews/?reviewed_movie_id=1')

        self.assertEqual(len(response.data), 2)
        for i in response.data:
            self.assertEqual(i['reviewed_movie'], 1)

        response_writer = self.client.get('/reviews/?writer_id=1')

        self.assertEqual(len(response_writer.data), 2)
        for i in response.data:
            self.assertEqual(i['writer'], 1)
