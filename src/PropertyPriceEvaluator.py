import argparse
import logging

from domain.Locations import generate_locations_across_area
from plotting.Heatmaps import WeightedHeatmap
from datasource.Nestoria import SearchCriteria, assess_locations


def parse_arguments():
    parser = argparse.ArgumentParser()
    log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
    log_levels.extend([level.lower() for level in log_levels])
    parser.add_argument("start_lat", help="Upper-left latitude coordinate for search area rectangle.", type=float)
    parser.add_argument("start_long", help="Upper-left longitude coordinate for search area rectangle.", type=float)
    parser.add_argument("end_lat", help="Lower-right latitude coordinate for search area rectangle.", type=float)
    parser.add_argument("end_long", help="Lower-right longitude coordinate for search area rectangle.", type=float)
    parser.add_argument("--step_lat", help="The step value between latitude points.")
    parser.add_argument("--long_step", help="The step value between longitude points.")
    parser.add_argument("--bedrooms_min", help="Minimum number of bedrooms.")
    parser.add_argument("--bedrooms_max", help="Maximum number of bedrooms.")
    parser.add_argument("--log", choices=log_levels)
    return parser.parse_args()


def set_logging_level(log_level_string):
    log_level = getattr(logging, log_level_string.upper(), None)
    logging.basicConfig(level=log_level)


def get_locations_from_args():
    if args.step_lat and args.long_step:
        locations = generate_locations_across_area(args.start_lat, args.start_long, args.end_lat, args.end_long, args.step_lat, args.long_step)
    elif args.step_lat:
        locations = generate_locations_across_area(args.start_lat, args.start_long, args.end_lat, args.end_long, step_latitude=args.step_lat)
    elif args.long_step:
        locations = generate_locations_across_area(args.start_lat, args.start_long, args.end_lat, args.end_long, step_longitude=args.long_step)
    else:
        locations = generate_locations_across_area(args.start_lat, args.start_long, args.end_lat, args.end_long)
    return locations


def main():
    search_criteria = SearchCriteria(bedrooms_min=args.bedrooms_min, bedrooms_max=args.bedrooms_max)
    locations = get_locations_from_args()
    weighted_coordinates = assess_locations(locations, search_criteria)
    heatmap = WeightedHeatmap(weighted_coordinates)
    logging.info("Generating heatmap...")
    heatmap.generate_weighted_heatmap(53.4800, -2.2430)


if __name__ == '__main__':
    args = parse_arguments()
    set_logging_level(args.log)
    main()
