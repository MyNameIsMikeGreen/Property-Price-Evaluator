import json
import logging
from statistics import mean

from domain.Locations import Location
from propertydata.provider.Provider import Provider, InvalidResponseError


class NestoriaProvider(Provider):

    BASE_URL = "https://api.nestoria.co.uk/api"
    BASE_PARAMS = {
        "encoding": "json",
        "action": "search_listings",
        "pretty": 1,
        "sort": "distance",
        "number_of_results": 50
    }

    def _search_listings(self, location: Location, search_criteria: dict):
        logging.debug(f"Searching listings for location on Nestoria: {str(location)}")
        search_criteria.update(self.BASE_PARAMS)
        search_criteria["centre_point"] = str(location)
        response = self._make_request(search_criteria)
        if not self._response_is_valid(response):
            raise InvalidResponseError("Request was unsuccessful.")
        response_content = json.loads(response.text)
        listings = response_content["response"]["listings"]
        logging.debug(f"{len(listings)} listings found for location: {str(location)}.")
        if len(listings) == 0:
            raise InvalidResponseError("0 listings found.")
        return listings

    def _average_listing_price(self, listings: list):
        return mean([listing["price"] for listing in listings])
