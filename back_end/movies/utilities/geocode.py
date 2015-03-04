import requests
import json
from movies.models import Location
import time

class geocode(object):
    def __init__(self):
        self.geo_api_key = "AIzaSyBXV0clkCxvKeJqCgY86THMqpiIMlNprfI"
        self.city = "San Francisco, CA"

    def get_coordinates(self, loc):
        res = self.get_response(loc)
        if res['status'] != "OK":
            return None, None
        res_location = res['results'][0]['geometry']['location']
        time.sleep(.25)
        return res_location['lat'], res_location['lng']

    def get_response(self, loc):
        endpoint = "https://maps.googleapis.com/maps/api/geocode/json?address=%s, %s&key=%s" % (loc, self.city, self.geo_api_key)
        res = requests.get(endpoint)
        if res.status_code != 200:
            raise Exception("Could not connect to SFD's servers")
        return res.json()

