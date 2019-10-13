import json
import logging
from statistics import mean
from time import sleep

import requests

from domain.Locations import Location, WeightedCoordinate

BASE_URL = "https://api.nestoria.co.uk/api"
BASE_PARAMS = {
    "encoding": "json",
    "action": "search_listings",
    "pretty": 1,
    "sort": "distance",
    "number_of_results": 50
}


class SearchCriteria(object):
    def __init__(self, bedrooms_min=0, bedrooms_max=100):
        self.bedrooms_min = bedrooms_min
        self.bedrooms_max = bedrooms_max


class InvalidResponseError(Exception):
    def __init__(self, message):
        self.message = message


def assess_locations(locations: list, search_criteria: dict):
    logging.info(f"Searching {len(locations)} locations...")
    weighted_coordinates = []
    for location in locations:
        listings = _search_listings(location, search_criteria)
        if len(listings) == 0:
            continue
        average = _average_listing_price(listings)
        logging.debug(f"Average listing price: {average}")
        weighting = _price_as_weighting(average)
        weighted_coordinate = WeightedCoordinate(location.latitude, location.longitude, weighting)
        logging.debug(f"Appending weighted coordinate: {str(weighted_coordinate)}")
        weighted_coordinates.append(weighted_coordinate)
        sleep(1)
    return weighted_coordinates


def _search_listings(location: Location, search_criteria: dict):
    logging.debug(f"Searching listings for location: {str(location)}")
    search_criteria.update(BASE_PARAMS)
    search_criteria["centre_point"] = str(location)
    response = requests.get(url=BASE_URL, params=search_criteria)
    if not _response_is_valid(response):
        raise InvalidResponseError("Request was unsuccessful.")
    response_content = json.loads(response.text)
    listings = response_content["response"]["listings"]
    logging.debug(f"{len(listings)} listings found for location: {str(location)}.")
    return listings


def _response_is_valid(response):
    if response.status_code != 200 \
            or response.reason != "OK"\
            or not response.text.strip():
        return False
    return True


def _average_listing_price(listings: list):
    return mean([listing["price"] for listing in listings])


def _price_as_weighting(price: int):
    return int(price/10000)
