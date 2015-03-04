from django.test import TestCase
from movies.models import Movie, Location, Person, ProductionCompany, Distributor
from movies.utilities.geocode import geocode

class GeocodeTestCase(TestCase):

    def setUp(self):
        self.geocode = geocode()

    def test_get_coordinates(self):
        loc_1 = "Golden Gate Park"
        loc_1_cords = {
            'lat' : 37.76904,
            'lng' : -122.4835193
        }
        loc_2 = "Epic Roasthouse (399 Embarcadero)"
        loc_2_cords = {
            'lat' : 37.7992627,
            'lng' : -122.3976732
        }
        result_1 = self.geocode.get_coordinates(loc_1)
        self.assertEqual(result_1[0], loc_1_cords['lat'])
        self.assertEqual(result_1[1], loc_1_cords['lng'])
        result_2 = self.geocode.get_coordinates(loc_2)
        self.assertEqual(result_2[0], loc_2_cords['lat'])
        self.assertEqual(result_2[1], loc_2_cords['lng'])
