from enum import Enum


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


class WeightedCoordinate(object):
    def __init__(self, latitude: float, longitude: float, weight: int):
        self.latitude = latitude
        self.longitude = longitude
        self.weight = weight

    def __str__(self):
        return f"({self.latitude},{self.longitude},{self.weight})"


def generate_locations_across_area(start_latitude, start_longitude, end_latitude, end_longitude, step_latitude=0.0005, step_longitude=0.0010):
    locations = []
    current_latitude = start_latitude
    while current_latitude < end_latitude:
        current_longitude = start_longitude
        while current_longitude < end_longitude:
            locations.append(Location(current_latitude, current_longitude, 0.5, Units.KILOMETERS))
            current_longitude += step_longitude
        current_latitude += step_latitude
    return locations
