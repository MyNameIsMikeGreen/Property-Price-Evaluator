import json
import logging
from statistics import mean
from time import sleep

import requests

from generator.LocationGenerator import Location

BASE_URL = "https://api.nestoria.co.uk/api"
BASE_PARAMS = {
    "encoding": "json",
    "action": "search_listings",
    "pretty": 1
}


class SearchCriteria(object):
    def __init__(self, bedrooms_min=0, bedrooms_max=100):
        self.bedrooms_min = bedrooms_min
        self.bedrooms_max = bedrooms_max


class InvalidResponseError(Exception):
    def __init__(self, message):
        self.message = message


class WeightedCoordinate(object):
    def __init__(self, latitude: float, longitude: float, weight: int):
        self.latitude = latitude
        self.longitude = longitude
        self.weight = weight

    def __str__(self):
        return f"({self.latitude},{self.longitude},{self.weight})"


def assess_locations(locations: list, search_criteria: SearchCriteria):
    logging.info("Searching locations...")
    logging.debug(f"{len(locations)} locations to be searched.")
    weighted_coordinates = []
    for location in locations:
        listings = search_listings(location, search_criteria)
        if len(listings) == 0:
            continue
        average = average_listing_price(listings)
        logging.debug(f"Average listing price: {average}")
        weighting = price_as_weighting(average)
        weighted_coordinate = WeightedCoordinate(location.latitude, location.longitude, weighting)
        logging.debug(f"Appending weighted coordinate: {str(weighted_coordinate)}")
        weighted_coordinates.append(weighted_coordinate)
        sleep(1)
    return weighted_coordinates


def search_listings(location: Location, search_criteria: SearchCriteria):
    logging.debug(f"Searching listings for location: {str(location)}")
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
    listings = response_content["response"]["listings"]
    logging.debug(f"{len(listings)} found.")
    return listings


def response_is_valid(response):
    if response.status_code != 200 \
            or response.reason != "OK"\
            or not response.text.strip():
        return False
    return True


def average_listing_price(listings: list):
    return mean([listing["price"] for listing in listings])


def price_as_weighting(price: int):
    return int(price/10000)
