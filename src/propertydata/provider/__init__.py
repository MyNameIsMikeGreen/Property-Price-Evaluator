from propertydata.provider.Nestoria import NestoriaProvider
from propertydata.provider.Zoopla import ZooplaProvider


class InvalidProviderError(Exception):
    pass


class ProviderFactory:

    @staticmethod
    def get_provider(name: str):
        normalised_name = name.lower().strip()
        if normalised_name == "nestoria":
            return NestoriaProvider()
        elif normalised_name == "zoopla":
            return ZooplaProvider()
        else:
            raise InvalidProviderError(name + " is not a supported provider.")
