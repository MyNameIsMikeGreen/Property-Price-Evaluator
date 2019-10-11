from datetime import datetime

import gmplot


class WeightedCoordinate(object):
    def __init__(self, latitude: float, longitude: float, weight: int):
        self.latitude = latitude
        self.longitude = longitude
        self.weight = weight


class WeightedHeatmap(object):

    def __init__(self):
        self.weighted_coordinates = []

    def generate_weighted_heatmap(self, latitude, longitude, zoom=13, filename=None):
        gmap = gmplot.GoogleMapPlotter(latitude, longitude, zoom)
        latitudes, longitudes = self._generate_weighted_coordinates_zip()
        gmap.heatmap(latitudes, longitudes)
        if not filename:
            filename = WeightedHeatmap._get_default_filename()
        gmap.draw(filename)

    def _generate_weighted_coordinates_zip(self):
        weighted_list = []
        for weighted_coordinate in self.weighted_coordinates:
            for i in range(0, weighted_coordinate.weight):
                weighted_list.append((weighted_coordinate.latitude, weighted_coordinate.longitude))
        return zip(*weighted_list)

    @staticmethod
    def _get_default_filename():
        date = datetime.today().strftime('%Y-%m-%d')
        return f"PropertyPriceEvaluator-mikegreen1995-{date}.html"
