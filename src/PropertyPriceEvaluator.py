import argparse
import logging

from generator.LocationGenerator import generate_locations
from generator.WeightedHeatmapGenerator import WeightedHeatmap
from generator.WeightedLocationGenerator import SearchCriteria, assess_locations


def parse_arguments():
    parser = argparse.ArgumentParser()
    log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
    log_levels.append([level.lower() for level in log_levels])
    parser.add_argument("--bedrooms_min", help="Minimum number of bedrooms.")
    parser.add_argument("--bedrooms_max", help="Maximum number of bedrooms.")
    parser.add_argument("--log", choices=log_levels)
    return parser.parse_args()


def set_logging_level(log_level_string):
    log_level = getattr(logging, log_level_string.upper(), None)
    logging.basicConfig(level=log_level)


def main():
    search_criteria = SearchCriteria(bedrooms_min=args.bedrooms_min, bedrooms_max=args.bedrooms_max)
    locations = generate_locations()
    weighted_coordinates = assess_locations(locations, search_criteria)
    heatmap = WeightedHeatmap(weighted_coordinates)
    logging.info("Generating heatmap...")
    heatmap.generate_weighted_heatmap(53.4800, -2.2430)


if __name__ == '__main__':
    args = parse_arguments()
    set_logging_level(args.log)
    main()
