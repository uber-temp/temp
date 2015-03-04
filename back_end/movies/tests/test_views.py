from django.test import TestCase
import json
from movies.models import Movie, Location, Person, ProductionCompany, Distributor

class MoviesViewsTestCase(TestCase):

    def setUp(self):
        pass

    def test_get_movies(self):
        response = self.client.get('/api/v1/movies/')
        self.assertEqual(response.status_code, 404)
        movie_1 = {
            "title" : "180",
            "actor_1" : "Siddarth",
            "locations" : "Epic Roasthouse (399 Embarcadero)",
            "release_year" : "2011",
            "production_company" : "SPI Cinemas",
            "actor_2" : "Nithya Menon",
            "writer" : "Umarji Anuradha, Jayendra, Aarthi Sriram, & Suba ",
            "director" : "Jayendra",
            "actor_3" : "Priya Anand"
        }
        director = Person.objects.create(name=movie_1['director'])
        title = movie_1['title']
        year = int(movie_1['release_year'])
        location = movie_1['locations']
        db_movie_1 = Movie.objects.create(title=title, year=year, director=director)
        Location.objects.create(name=location, latitude=0, longitude=0, movie=db_movie_1)
        response = self.client.get('/api/v1/movies/')
        res_dict = json.loads(response.content)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['id'], 1)
        self.assertEqual(res_dict[0]['title'], '180')
        self.assertEqual(res_dict[0]['locations'][0]['id'], 1)
        movie_2 = {
            "title" : "50 First Dates",
            "actor_1" : "Adam Sandler",
            "locations" : "Golden Gate Park",
            "release_year" : "2004",
            "production_company" : "Columbia Pictures Corporation",
            "distributor" : "Columbia Pictures",
            "actor_2" : "Nithya Menon",
            "writer" : "George Wing",
            "director" : "Peter Segal"
        }
        director = Person.objects.create(name=movie_2['director'])
        title = movie_2['title']
        year = int(movie_2['release_year'])
        location = movie_2['locations']
        db_movie_2 = Movie.objects.create(title=title, year=year, director=director)
        Location.objects.create(name=location, latitude=0, longitude=0, movie=db_movie_2)
        response = self.client.get('/api/v1/movies/')
        res_dict = json.loads(response.content)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(res_dict[1]['id'], 2)
        self.assertEqual(res_dict[1]['title'], '50 First Dates')
        self.assertEqual(res_dict[1]['locations'][0]['id'], 2)

    def test_get_locations(self):
        response = self.client.get('/api/v1/locations/')
        self.assertEqual(response.status_code, 404)
        director = Person.objects.create(name='test')
        movie = Movie.objects.create(title='test', year=1999, director=director)
        Location.objects.create(name='test1', latitude=50, longitude=40, movie=movie)
        Location.objects.create(name='test2', latitude=20, longitude=0, movie=movie)
        response = self.client.get('/api/v1/locations/')
        res_dict = json.loads(response.content)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(res_dict[0]['id'], 1)
        self.assertEqual(res_dict[0]['name'], 'test1')
        self.assertEqual(res_dict[0]['latitude'], "50.00")
        self.assertEqual(res_dict[0]['longitude'], "40.00")
        self.assertEqual(res_dict[0]['movie'], 1)

    def test_get_movie(self):
        response = self.client.get('/api/v1/movies/1')
        self.assertEqual(response.status_code, 404)
        director = Person.objects.create(name='test director')
        actor = Person.objects.create(name='test actor')
        production_company = ProductionCompany.objects.create(name='test pc')
        db_movie = Movie.objects.create(title='test', year=1999, director=director, production_company=production_company)
        db_movie.actors.add(actor)
        db_movie.save()
        response = self.client.get('/api/v1/movies/1')
        self.assertEqual(response.status_code, 200)
        res_dict = json.loads(response.content)
        self.assertEqual(res_dict['id'], 1)
        self.assertEqual(res_dict['director']['name'], 'test director')
        self.assertEqual(res_dict['title'], 'test')
        self.assertEqual(res_dict['production_company']['name'], 'test pc')
        self.assertEqual(res_dict['actors'][0]['name'], 'test actor')

        


