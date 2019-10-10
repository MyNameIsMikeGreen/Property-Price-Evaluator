import json
from enum import Enum

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


def search_listings(bedrooms_min: int, bedrooms_max: int, location: Location):
    params = {
        "bedrooms_min": bedrooms_min,
        "bedrooms_max": bedrooms_max,
        "centre_point": str(location)
    }
    params.update(BASE_PARAMS)
    return requests.get(url=BASE_URL, params=params)


def evaluate_location():
    response = search_listings(2, 2, Location(53.4808, -2.2426, 0.5, Units.KILOMETERS))
    return json.loads(response.text)


if __name__ == '__main__':
    evaluation = evaluate_location()
