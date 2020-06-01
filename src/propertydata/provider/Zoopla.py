import json
import logging
from statistics import mean

from domain.Locations import Location
from propertydata.provider.Provider import Provider, InvalidResponseError


class ZooplaProvider(Provider):

    BASE_URL = "https://api.zoopla.co.uk/api/v1/property_listings.js"
    with open('../zoopla_api_key.txt', 'r') as file:
        api_key = file.read()
    BASE_PARAMS = {
        "api_key": api_key  # TODO: Make a nicer way of passing in API keys
    }

    def _search_listings(self, location: Location, search_criteria: dict):
        logging.debug(f"Searching listings for location on Zoopla: {str(location)}")
        search_criteria.update(self.BASE_PARAMS)
        search_criteria["latitude"] = location.latitude
        search_criteria["longitude"] = location.longitude
        search_criteria["radius"] = location.radius
        response = self._make_request(search_criteria)
        if not self._response_is_valid(response):
            raise InvalidResponseError("Request was unsuccessful (HTTP " + response.status_code + "- " + response.reason + ").")
        response_content = json.loads(response.text)
        listings = response_content["listing"]
        logging.debug(f"{len(listings)} listings found for location: {str(location)}.")
        if len(listings) == 0:
            raise InvalidResponseError("0 listings found.")
        return listings

    def _average_listing_price(self, listings: list):
        return mean([int(listing["price"]) for listing in listings])
