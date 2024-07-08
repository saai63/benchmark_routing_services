from abc import ABC, abstractmethod
from functools import wraps
from prettytable import PrettyTable
import json
import os
import requests
import time
import uuid

OLA_API_KEY = "OLA_API_KEY"
MB_API_KEY = "MB_API_KEY"
TT_API_KEY = "TT_API_KEY"
HERE_API_KEY = "HERE_API_KEY"


def calculate_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        time_taken_ms = (end_time - start_time) * 1000
        return result, time_taken_ms

    return wrapper


def get_api_keys_or_terminate(key_name):
    api_key_value = os.environ.get(key_name)
    if api_key_value is None:
        print("Environment variable " + key_name + " is not set. Exiting.")
        exit()
    return api_key_value


class GisInterface(ABC):
    @abstractmethod
    def calculate_route(self, origin, destination):
        pass


def get_location_as_string(location_tuple, reverse=False):
    if reverse:
        return "{}%2C{}".format(location_tuple[1], location_tuple[0])
    return "{},{}".format(location_tuple[0], location_tuple[1])


class Ola(GisInterface):
    def __init__(self):
        self.api_key = get_api_keys_or_terminate(OLA_API_KEY)

    @calculate_time
    def calculate_route(self, origin, destination):
        url = 'https://api.olamaps.io/routing/v1/directions'
        options = {
            'origin': get_location_as_string(origin),
            'destination': get_location_as_string(destination),
            'alternatives': True,
            'steps': True,
            'overview': 'full',
            'language': 'en',
            'traffic_metadata': False,
            'api_key': self.api_key
        }
        headers = {
            'accept': 'application/json'
        }
        r = requests.post(url, params=options)
        if r.status_code != 200:
            print("Route calculation using {} failed with error code {} and error {}".format(self.__class__.__name__,
                                                                                             r.status_code, r.text))
            exit()
        return r


class Mapbox(GisInterface):

    def __init__(self):
        self.api_key = get_api_keys_or_terminate(MB_API_KEY)

    @calculate_time
    def calculate_route(self, origin, destination):
        url = 'https://api.mapbox.com/directions/v5/mapbox/driving/' + get_location_as_string(
            origin, True) + '%3B' + get_location_as_string(destination, True)
        options = {
            'alternatives': 'true',
            'annotations': 'distance,duration',
            'steps': 'true',
            'banner_instructions': 'true',
            'geometries': 'geojson',
            'language': 'en',
            'overview': 'full',
            'access_token': self.api_key
        }
        headers = {
            'accept': 'application/json'
        }
        r = requests.get(url, params=options)
        if r.status_code != 200:
            print("Route calculation using {} failed with error code {} and error {}".format(self.__class__.__name__,
                                                                                             r.status_code, r.text))
            exit()
        return r


class TomTom(GisInterface):

    def __init__(self):
        self.api_key = get_api_keys_or_terminate(TT_API_KEY)

    @calculate_time
    def calculate_route(self, origin, destination):
        url = 'https://api.tomtom.com/routing/1/calculateRoute/' + get_location_as_string(
            origin) + ':' + get_location_as_string(destination) + '/json'
        options = {
            'instructionsType': 'coded',
            'instructionPhonetics': 'IPA',
            'guidanceVersion': 1,
            'language': 'en-US',
            'routeRepresentation': 'polyline',
            'key': self.api_key,
        }
        r = requests.get(url, params=options)
        if r.status_code != 200:
            print("Route calculation using {} failed with error code {} and error {}".format(self.__class__.__name__,
                                                                                             r.status_code, r.text))
            exit()
        return r


class Here(GisInterface):
    def __init__(self):
        self.api_key = get_api_keys_or_terminate(HERE_API_KEY)

    @calculate_time
    def calculate_route(self, origin, destination):
        url = 'https://router.hereapi.com/v8/routes'
        options = {
            'transportMode': 'car',
            'origin': get_location_as_string(origin),
            'destination': get_location_as_string(destination),
            'return': 'polyline,instructions,actions',
            'lang': 'en-US',
            'apiKey': self.api_key
        }
        headers = {
            # 'accept': 'application/json',
            'X-Request-ID': uuid.uuid4()
        }
        r = requests.get(url, params=options)
        if r.status_code != 200:
            print("Route calculation using {} failed with error code {} and error {}".format(self.__class__.__name__,
                                                                                             r.status_code, r.text))
            exit()
        return r


mumbai_cst = (18.939791, 72.834929)
bangalore_majestic = (12.977366, 77.570826)
# berlin_hbf = (52.525882, 13.367883)
# amsterdam_central = (52.379199, 4.897506)
GIS_services = [Ola(), Mapbox(), TomTom(), Here()]
table_view = PrettyTable()
table_view.field_names = ["Service Provider", "Service", "Time taken (in ms)"]
for gis_service in GIS_services:
    packed_response = gis_service.calculate_route(mumbai_cst, bangalore_majestic)
    response = packed_response[0]
    time_taken = packed_response[1]
    if response is not None:
        backend = gis_service.__class__.__name__
        table_view.add_row([backend, "Calculate route", time_taken])
        # print('{} returned a response of size {}'.format(backend, len(response.content)))
        file_name = backend + '.json'
        with open(file_name, 'w') as file:
            json.dump(response.json(), file, indent=2)
print(table_view)
