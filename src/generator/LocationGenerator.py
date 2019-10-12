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


def generate_locations():
    locations = []
    for x in range(0, 5):
        longitude = -2.2430 + (float(x) * 0.0005)
        for y in range(0, 5):
            latitude = 53.4800 + (float(y) * 0.0005)
            locations.append(Location(latitude, longitude, 0.5, Units.KILOMETERS))
    return locations
