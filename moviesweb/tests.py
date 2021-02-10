from django.contrib.auth.views import LoginView
from django.test import TestCase, Client
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APITestCase
import tmdbsimple as tmdb

from moviesweb.views import movies, signup, logout_request


class URLTest(TestCase):
    def test_movies_url(self):
        url = reverse('movies')
        self.assertEqual(resolve(url).func, movies)

        client = Client()
        response = client.get(reverse('movies'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.__name__, LoginView.__name__)

        client = Client()
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.__name__, signup.__name__)

        client = Client()
        response = client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.__name__, logout_request.__name__)

        client = Client()
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class MovieTest(APITestCase):
    client = APIClient()

    def test_post_movie_with_own_description(self):
        response = self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'MOJ TESTOWY OPIS'
        })
        self.assertEqual(response.data['title'], 'cat')
        self.assertEquals(response.data['description'], 'MOJ TESTOWY OPIS')
        self.assertEqual(response.status_code, 201)

    def test_post_movie_with_description_tmdb(self):
        title = 'Joker'
        response = self.client.post('/my_movies/', data={
            'title': title, 'description': ''
        })

        description_from_tmdb = tmdb.Search().movie(query=title)['results'][0]['overview']

        self.assertEqual(response.data['title'], 'Joker')
        self.assertEquals(response.data['description'], description_from_tmdb)
        self.assertEqual(response.status_code, 201)

    def test_post_movie_no_title(self):
        response = self.client.post('/my_movies/', data={
            'title': '', 'description': ''
        })
        self.assertEqual(response.status_code, 400)

    def test_get_movies(self):
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ala ma kota',
        })
        self.client.post('/my_movies/', data={
            'title': 'django', 'description': 'ala ma kota',
        })
        response = self.client.get('/my_movies/')
        self.assertEqual(len(response.data), 2)


class CommentTest(APITestCase):
    client = APIClient()

    def test_post_comment(self):
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ala ma kota',
        })
        response = self.client.post('/comments/', data={
            'movie': '1', 'comment_text': 'ala ma psa'
        })
        self.assertEqual(response.data['movie'], 1)
        self.assertEqual(response.data['comment_text'], 'ala ma psa')

    def test_get_comments(self):
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ala ma kota',
        })
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'ala ma kota'})
        self.client.post('/comments/', data={'movie': '1', 'comment_text': 'ala ma psa'})
        response = self.client.get('/comments/')
        self.assertEqual(len(response.data), 2)

    def test_get_filtered_comments(self):
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
    client = APIClient()

    def test_post_review(self):
        self.client.post('/my_movies/', data={
            'title': 'cat', 'description': 'ads',
        })

        self.client.post('/users/', data={
            'username': 'sddsf', 'email': 'dawid100298@o2.pl',
        })

        response = self.client.post('/reviews/', data={
            'review_title': 'Batman', 'content': 'ala ma kota', 'rating': '10', 'writer': '1',
            'reviewed_movie': '1',
        })

        self.assertEqual(response.data['review_title'], 'Batman')
        self.assertEqual(response.data['content'], 'ala ma kota')
        self.assertEqual(response.data['rating'], 10)
        self.assertEqual(response.data['writer'], 1)
        self.assertEqual(response.data['reviewed_movie'], 1)

    def test_get_review(self):
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

    def test_get_filtered_comments(self):
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
