# Get-my-movies
Web application written in python with Django framework for browsing movies provided by The Movie Database (TMDb). 

The application also displays the ranking of movies added to our database.

Extracting and adding data from and to our database is possible thanks to api provided by the application by using django restframework.


## Run application

To use our application you need to clone this repository:

$ git clone https://github.com/DawidSzczerba/get_my_movies

Then you need to apply the already created database migrations:

$ python manage.py migrate

And then run the application via the command:

$ python manage.py runserver


##  API
If you run the application locally, the api provides the following addresses:

"users": "http://127.0.0.1:8000/users/",
"my_movies": "http://127.0.0.1:8000/my_movies/",
"comments": "http://127.0.0.1:8000/comments/",
"reviews": "http://127.0.0.1:8000/reviews/"

The available commands are:
GET, POST, HEAD, OPTIONS

You can search for a movie by title:
http://127.0.0.1:8000/my_movies/?title=[write_here_movie_title]

You can search for comments of a particular movie:
http://127.0.0.1:8000/comments/?movie_id=[write_here_movie_id]

You can search for reviews/ratings of a particular movie:
http://127.0.0.1:8000/reviews/?reviewed_movie_id=[write_here_movie_id]

You can search for ratings by user:
http://127.0.0.1:8000/reviews/?writer_id=[write_here_user_id]
