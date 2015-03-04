from django.test import TestCase
from movies.models import Movie, Location, Person, ProductionCompany, Distributor
from movies.utilities.importer import SFD_Importer


class ImporterTestCase(TestCase):

    def setUp(self):
        self.importer = SFD_Importer()


    def test_get_actors(self):
        actor_1 = "actor 1"
        actor_2 = "actor 2"
        actor_3 = "actor 3"
        test_actors_0 = {}
        test_actors_1 = {'actor_1':actor_1}
        test_actors_2 = {'actor_1':actor_1, 'actor_2':actor_2}
        test_actors_3 = {'actor_1':actor_1,'actor_2':actor_2,'actor_3':actor_3}
        db_actor_1 = Person.objects.create(name=actor_1)
        db_actor_2 = Person.objects.create(name=actor_2)
        db_actor_3 = Person.objects.create(name=actor_3)
        self.assertEqual(self.importer.get_actors(test_actors_0), None)
        self.assertEqual(self.importer.get_actors(test_actors_1), (db_actor_1,))
        self.assertEqual(self.importer.get_actors(test_actors_2), (db_actor_1, db_actor_2))
        self.assertEqual(self.importer.get_actors(test_actors_3), (db_actor_1, db_actor_2, db_actor_3))

    def test_add_movie(self):
        movie = {
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
        self.importer.add_movie(movie)
        self.assertEqual(Movie.objects.all().count(), 1)
        db_movie = Movie.objects.get(id=1)
        self.assertEqual(db_movie.title, movie['title'])
        self.assertEqual(db_movie.director.name, movie['director'])
        self.assertEqual(db_movie.writer.name, movie['writer'])
        self.assertEqual(db_movie.year, int(movie['release_year']))
        self.assertEqual(db_movie.locations.all()[0].name, movie['locations'])
        db_actors = db_movie.actors.all().order_by('id')
        self.assertEqual(db_actors.count(), 3)
        self.assertEqual(db_actors[0].name, movie['actor_1'])
        self.assertEqual(db_actors[1].name, movie['actor_2'])
        self.assertEqual(db_actors[2].name, movie['actor_3'])

    def test_fill_data(self):
        movies = [{
            "title" : "180",
            "actor_1" : "Siddarth",
            "locations" : "Epic Roasthouse (399 Embarcadero)",
            "release_year" : "2011",
            "production_company" : "SPI Cinemas",
            "actor_2" : "Nithya Menon",
            "writer" : "Umarji Anuradha, Jayendra, Aarthi Sriram, & Suba ",
            "director" : "Jayendra",
            "actor_3" : "Priya Anand"
            },
            {
            "title" : "180",
            "actor_1" : "Siddarth",
            "locations" : "Mason & California Streets (Nob Hill)",
            "release_year" : "2011",
            "production_company" : "SPI Cinemas",
            "actor_2" : "Nithya Menon",
            "writer" : "Umarji Anuradha, Jayendra, Aarthi Sriram, & Suba ",
            "director" : "Jayendra",
            "actor_3" : "Priya Anand"
            },
            {
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
        ]
        self.importer.data = movies
        self.importer.fill_data()
        self.assertEqual(Movie.objects.all().count(), 2)
        db_movie_1 = Movie.objects.get(id=1)
        self.assertEqual(db_movie_1.title, movies[0]['title'])
        self.assertEqual(db_movie_1.year, int(movies[0]['release_year']))
        self.assertEqual(db_movie_1.production_company.name, movies[0]['production_company'])
        self.assertEqual(db_movie_1.director.name, movies[0]['director'])
        self.assertEqual(db_movie_1.writer.name, movies[0]['writer'])
        self.assertEqual(db_movie_1.locations.all().count(), 2)
        # + 1 because director is created first
        self.assertEqual(Person.objects.get(id=1+1).name, movies[0]['actor_1'])
        self.assertEqual(Person.objects.get(id=2+1).name, movies[0]['actor_2'])
        self.assertEqual(Person.objects.get(id=3+1).name, movies[0]['actor_3'])
        # + 3 because director and writer were added from first movie, and director was added from second movie
        self.assertEqual(Person.objects.get(id=4+3).name, movies[2]['actor_1'])
        self.assertEqual(Person.objects.get(id=2+1).name, movies[2]['actor_2'])
        for i, movie in enumerate(movies):
            db_location = Location.objects.get(id=i+1)
            self.assertEqual(db_location.name, movie['locations'])
