import requests
import json
from movies.models import Movie, Location, Person, ProductionCompany, Distributor
from movies.utilities.geocode import geocode
from django.db.utils import IntegrityError

class SFD_Importer(object):
    def __init__(self):
        self.sfd_api = "https://data.sfgov.org/resource/yitu-d5am.json?$limit=50000"
        self.geocode = geocode()

    def runner(self):
        self.data = self.get_data()
        self.fill_data()

    def get_data(self):
        res = requests.get(self.sfd_api)
        if res.status_code != 200:
            raise Exception("Could not connect to SFD's servers")
        return res.json()

    def fill_data(self):
        for movie in self.data:
            self.add_movie(movie)

    def add_movie(self, sfd_movie):
        title = sfd_movie['title']
        year = int(sfd_movie['release_year'])
        director_name = sfd_movie['director']
        director, director_created = Person.objects.get_or_create(name=director_name)

        movie, movie_created = Movie.objects.get_or_create(title=title, year=year, director=director)

        actors = self.get_actors(sfd_movie)
        if actors:
            movie.actors.add(*actors)

        if 'distributor' in sfd_movie:
            dist_name = sfd_movie['distributor']
            dist, dist_created = Distributor.objects.get_or_create(name=dist_name)
            movie.distributor = dist

        if 'production_company' in sfd_movie:
            prod_name = sfd_movie['production_company']
            prod, prod_created = ProductionCompany.objects.get_or_create(name=prod_name)
            movie.production_company = prod

        if 'writer' in sfd_movie:
            writer_name = sfd_movie['writer']
            writer, writer_created = Person.objects.get_or_create(name=writer_name)
            movie.writer = writer

        if 'locations' in sfd_movie:
            loc_name = sfd_movie['locations']
            try:
                Location.objects.get(name=loc_name, movie=movie)
            except Location.DoesNotExist:
                lat, lng = self.geocode.get_coordinates(loc_name)
                if lat != None:
                    Location.objects.create(name=loc_name, latitude=lat, longitude=lng, movie=movie)
        movie.save()

    def get_actors(self, sfd_movie):
        if 'actor_1' not in sfd_movie:
            return None
        def create_actor(actor_num):
            actor_name = sfd_movie[actor_num]
            actor, actor_created = Person.objects.get_or_create(name=actor_name)
            return (actor,)
        actors = create_actor('actor_1')
        if 'actor_2' in sfd_movie:
            actors = actors + create_actor('actor_2')
        if 'actor_3' in sfd_movie:
            actors = actors + create_actor('actor_3')
        return actors

    

