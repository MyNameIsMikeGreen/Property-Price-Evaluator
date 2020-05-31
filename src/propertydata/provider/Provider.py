import logging
from abc import ABC, abstractmethod
from time import sleep

import requests
from requests import Response

from domain.Locations import Location, WeightedCoordinate


class InvalidResponseError(Exception):
    def __init__(self, message):
        self.message = message


class Provider(ABC):

    BASE_URL = ""
    BASE_PARAMS = {}

    def __init__(self):
        super().__init__()

    def assess_locations(self, locations: list, search_criteria: dict, sleep_secs: int):
        logging.info(f"Searching {len(locations)} locations...")
        weighted_coordinates = []
        for location in locations:
            try:
                listings = self._search_listings(location, search_criteria)
                weighted_coordinate = self._listings_as_weighted_coordinate(listings, location)
            except Exception as e:
                logging.warning("Unsuccessful search for location: " + str(location))
                sleep(sleep_secs)
                continue
            logging.debug(f"Appending weighted coordinate: {str(weighted_coordinate)}")
            weighted_coordinates.append(weighted_coordinate)
            sleep(sleep_secs)
        return weighted_coordinates

    def _make_request(self, search_criteria: dict, iteration=1):
        try:
            return requests.get(url=self.BASE_URL, params=search_criteria)
        except Exception as e:
            if iteration < 3:
                logging.warning(f"Failed to make request ({iteration}). Sleeping before retry...")
                sleep(15)
                return self._make_request(search_criteria, iteration + 1)
            else:
                logging.error("Failed to make request after 3 attempts. Aborting.")
                exit(-1)

    def _listings_as_weighted_coordinate(self, listings, location):
        average = self._average_listing_price(listings)
        logging.debug(f"Average listing price: {average}")
        weighting = self._price_as_weighting(average)
        weighted_coordinate = WeightedCoordinate(location.latitude, location.longitude, weighting)
        return weighted_coordinate

    @abstractmethod
    def _search_listings(self, location: Location, search_criteria: dict):
        pass

    @abstractmethod
    def _average_listing_price(self, listings: list):
        pass

    @staticmethod
    def _price_as_weighting(price: int):
        return int(price / 10000)

    @staticmethod
    def _response_is_valid(response: Response):
        if response.status_code != 200 \
                or response.reason != "OK" \
                or not response.text.strip():
            return False
        return True
