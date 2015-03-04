# Personal
[Personal Site](http://nickincardone.com)

[Github](https://github.com/nickincardone)

[LinkedIn](http://www.linkedin.com/in/nickincardone)

# Challenge
[Live Site](http://nickincardone.com/uber/)

## about
I chose to implement the SF Movies task on the back-end track with a minimal front-end page. I originally intended to go full-stack but due to time constraints (please note I am currently employed) the back-end got most of the work.

## back-end
I chose to use django as my back-end framework with the django-rest-framework package. I filled the db (which is in sqlite since the project is small) using the SFD and Google Geocode api to get the movie information and location coordinates. I created three endpoints `/api/v1/movies`, `/api/v1/locations`, and `/api/v1/movies/{id}`. The first endpoint returns all the movies ids, titles, and location ids associated with them. The second endpoint returns all the locations with their id, coordinates, and title. The last endpoint returns all information for a specific movie (director, actors, etc). This design with this particular project in mind, so the endpoints are read only and were seperated to reduce load times for the front-end.

to run locally from source directory
```
cd back_end
pip install -r requirements.txt
python manage.py runserver
```

## front-end
I have the most experience developing applications using angular.js, but since the challenge specifically suggested not to use it I decided to use vanilla jQuery. The logic flow of the app is on load a call is made to the `/api/v1/movies` endpoint which populates a movies array and once that is loaded a second call is made to `api/v1/locations` to initialize a locations array. The movie array is used to create a list of movies, with each <li> element having an attribute of the id of its movie. When a movie is clicked by the user it clears all markers on an earlier initialized map (if any), gets the locations associated with that movie, and places the markers corresponding to these locations on the map. Additionally, a call is made to `api/v1/movies/{id}` to get all the movie information to display to the user. The application could be developed using a single endpoint that brings in all the neccesary information, but it was designed in a way that could handle larger data without much higher latency.

Note: I focused most of my time on the back-end so the the front-end is bare.

## testing
There are only unit tests for the back-end project.

You can run tests with `python manage.py test` and you can view test 
coverage by opening `back_end/htmlcov/index.html` in your browser.