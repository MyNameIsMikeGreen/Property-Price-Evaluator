import json
from enum import Enum
from statistics import mean

import requests as requests


BASE_URL = "https://api.nestoria.co.uk/api"
BASE_PARAMS = {
    "encoding": "json",
    "action": "search_listings",
    "pretty": 1
}


class Units(Enum):
    KILOMETERS = "km"
    MILES = "mi"

    def __str__(self):
        return str(self.value)


class Location(object):
    def __init__(self, latitude: float, longitude: float, radius: float, units: Units):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.units = units

    def __str__(self):
        return f"{self.latitude},{self.longitude},{self.radius}{self.units}"


class SearchCriteria(object):
    def __init__(self, bedrooms_min=0, bedrooms_max=100):
        self.bedrooms_min = bedrooms_min
        self.bedrooms_max = bedrooms_max


class InvalidResponseError(Exception):
    def __init__(self, message):
        self.message = message


def search_listings(location: Location, search_criteria: SearchCriteria):
    params = {
        "bedrooms_min": search_criteria.bedrooms_min,
        "bedrooms_max": search_criteria.bedrooms_max,
        "centre_point": str(location)
    }
    params.update(BASE_PARAMS)
    response = requests.get(url=BASE_URL, params=params)
    if not response_is_valid(response):
        raise InvalidResponseError("Request was unsuccessful.")
    response_content = json.loads(response.text)
    return response_content["response"]["listings"]


def response_is_valid(response):
    if response.status_code != 200 \
            or response.reason != "OK"\
            or not response.text.strip():
        return False
    return True


def average_listing_price(listings: list):
    return mean([listing["price"] for listing in listings])


if __name__ == '__main__':
    location = Location(53.4808, -2.2426, 0.5, Units.KILOMETERS)
    listings = search_listings(location, SearchCriteria(bedrooms_min=2, bedrooms_max=2))
    average = average_listing_price(listings)
