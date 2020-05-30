import json
import logging
from statistics import mean
from time import sleep

import requests
from requests import Response

from domain.Locations import Location, WeightedCoordinate

# TODO: Split into different files for each provider
NESTORIA_BASE_URL = "https://api.nestoria.co.uk/api"
NESTORIA_BASE_PARAMS = {
    "encoding": "json",
    "action": "search_listings",
    "pretty": 1,
    "sort": "distance",
    "number_of_results": 50
}

ZOOPLA_BASE_URL = "https://api.zoopla.co.uk/api/v1/property_listings.js"
with open('../zoopla_api_key.txt', 'r') as file:
    api_key = file.read()
ZOOPLA_BASE_PARAMS = {
    "api_key": api_key  # TODO: Make a nicer way of passing in API keys
}


class SearchCriteria(object):
    def __init__(self, bedrooms_min=0, bedrooms_max=100):
        self.bedrooms_min = bedrooms_min
        self.bedrooms_max = bedrooms_max


class InvalidResponseError(Exception):
    def __init__(self, message):
        self.message = message


def assess_locations(locations: list, search_criteria: dict, sleep_secs: int = 1, provider="Nestoria"):
    logging.info(f"Searching {len(locations)} locations...")
    weighted_coordinates = []
    for location in locations:
        try:
            if provider == "Nestoria":  # TODO: Strengthen provider passing
                listings = _search_nestoria_listings(location, search_criteria)  # TODO: Reduce duplication in if-blocks
                weighted_coordinate = _nestoria_listings_as_weighted_coordinate(listings, location)
            elif provider == "Zoopla":
                listings = _search_zoopla_listings(location, search_criteria)
                weighted_coordinate = _zoopla_listings_as_weighted_coordinate(listings, location)
            else:
                logging.error("Invalid API provider selected. Aborting.")
                exit(-1)
        except:
            logging.warning("Unsuccessful search for location: " + str(location))
            sleep(sleep_secs)
            continue
        logging.debug(f"Appending weighted coordinate: {str(weighted_coordinate)}")
        weighted_coordinates.append(weighted_coordinate)
        sleep(sleep_secs)
    return weighted_coordinates


def _nestoria_listings_as_weighted_coordinate(listings, location):
    average = _nestoria_average_listing_price(listings)
    logging.debug(f"Average listing price: {average}")
    weighting = _price_as_weighting(average)
    weighted_coordinate = WeightedCoordinate(location.latitude, location.longitude, weighting)
    return weighted_coordinate


def _search_nestoria_listings(location: Location, search_criteria: dict):
    logging.debug(f"Searching listings for location on Nestoria: {str(location)}")
    search_criteria.update(NESTORIA_BASE_PARAMS)
    search_criteria["centre_point"] = str(location)
    response = _make_request(NESTORIA_BASE_URL, search_criteria)
    if not _response_is_valid(response):
        raise InvalidResponseError("Request was unsuccessful.")
    response_content = json.loads(response.text)
    listings = response_content["response"]["listings"]
    logging.debug(f"{len(listings)} listings found for location: {str(location)}.")
    if len(listings) == 0:
        raise InvalidResponseError("0 listings found.")
    return listings


def _zoopla_listings_as_weighted_coordinate(listings, location):
    average = _zoopla_average_listing_price(listings)
    logging.debug(f"Average listing price: {average}")
    weighting = _price_as_weighting(average)
    weighted_coordinate = WeightedCoordinate(location.latitude, location.longitude, weighting)
    return weighted_coordinate


def _search_zoopla_listings(location: Location, search_criteria: dict):
    logging.debug(f"Searching listings for location on Zoopla: {str(location)}")
    search_criteria.update(ZOOPLA_BASE_PARAMS)
    search_criteria["latitude"] = location.latitude
    search_criteria["longitude"] = location.longitude
    search_criteria["radius"] = location.radius
    response = _make_request(ZOOPLA_BASE_URL, search_criteria)
    if not _response_is_valid(response):
        raise InvalidResponseError("Request was unsuccessful.")
    response_content = json.loads(response.text)
    listings = response_content["listing"]
    logging.debug(f"{len(listings)} listings found for location: {str(location)}.")
    if len(listings) == 0:
        raise InvalidResponseError("0 listings found.")
    return listings


def _make_request(url, search_criteria: dict, iteration=1):
    try:
        return requests.get(url=url, params=search_criteria)
    except Exception as e:
        if iteration < 3:
            logging.warning(f"Failed to make request ({iteration}). Sleeping before retry...")
            sleep(15)
            return _make_request(search_criteria, iteration + 1)
        else:
            logging.error("Failed to make request after 3 attempts. Aborting.")
            exit(-1)


def _response_is_valid(response: Response):
    if response.status_code != 200 \
            or response.reason != "OK" \
            or not response.text.strip():
        return False
    return True


def _nestoria_average_listing_price(listings: list):
    return mean([listing["price"] for listing in listings])


def _zoopla_average_listing_price(listings: list):
    return mean([int(listing["price"]) for listing in listings])


def _price_as_weighting(price: int):
    return int(price / 10000)
