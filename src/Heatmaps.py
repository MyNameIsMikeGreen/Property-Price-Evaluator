import ntpath
from datetime import datetime
from os import makedirs
from os.path import isdir

import gmplot


class WeightedHeatmap(object):

    def __init__(self, weighted_coordinates=None):
        self.weighted_coordinates = weighted_coordinates

    def generate_weighted_heatmap(self, latitude, longitude, zoom=13, filename=None):
        gmap = gmplot.GoogleMapPlotter(latitude, longitude, zoom)
        latitudes, longitudes = self._generate_weighted_coordinates_zip()
        gmap.heatmap(latitudes, longitudes)
        if not filename:
            filename = WeightedHeatmap._get_default_filename()
            self._make_directory_if_not_exists(filename)
        gmap.draw(filename)

    def _generate_weighted_coordinates_zip(self):
        weighted_list = []
        for weighted_coordinate in self.weighted_coordinates:
            for i in range(0, weighted_coordinate.weight):
                weighted_list.append((weighted_coordinate.latitude, weighted_coordinate.longitude))
        return zip(*weighted_list)

    @staticmethod
    def _make_directory_if_not_exists(filename):
        basename = ntpath.dirname(filename)
        if not isdir(basename):
            makedirs(basename)

    @staticmethod
    def _get_default_filename():
        date = datetime.today().strftime('%Y-%m-%d')
        return f"output/PropertyPriceEvaluator-mikegreen1995-{date}.html"
