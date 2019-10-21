import argparse
import json
import logging

from datasource.Nestoria import assess_locations
from domain.Locations import generate_locations_across_area
from plotting.Heatmaps import WeightedHeatmap


def parse_arguments():
    parser = argparse.ArgumentParser()
    log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
    log_levels.extend([level.lower() for level in log_levels])
    parser.add_argument("start_lat", help="Upper-left latitude coordinate for search area rectangle.", type=float)
    parser.add_argument("start_long", help="Upper-left longitude coordinate for search area rectangle.", type=float)
    parser.add_argument("end_lat", help="Lower-right latitude coordinate for search area rectangle.", type=float)
    parser.add_argument("end_long", help="Lower-right longitude coordinate for search area rectangle.", type=float)
    parser.add_argument("--step_lat", help="The step value between latitude points.", type=float)
    parser.add_argument("--step_long", help="The step value between longitude points.", type=float)
    parser.add_argument("--search_params_file", help="Path to search filter file, json formatted.")
    parser.add_argument("--sleep_secs", help="Seconds to sleep between searches.", type=float, default=1)
    parser.add_argument("--log", choices=log_levels)
    return parser.parse_args()


def set_logging_level(log_level_string):
    log_level = getattr(logging, log_level_string.upper(), None)
    logging.basicConfig(level=log_level)


def get_locations_from_args():
    if args.step_lat and args.step_long:
        locations = generate_locations_across_area(args.start_lat, args.start_long, args.end_lat, args.end_long,
                                                   args.step_lat, args.step_long)
    elif args.step_lat:
        locations = generate_locations_across_area(args.start_lat, args.start_long, args.end_lat, args.end_long,
                                                   step_latitude=args.step_lat)
    elif args.step_long:
        locations = generate_locations_across_area(args.start_lat, args.start_long, args.end_lat, args.end_long,
                                                   step_longitude=args.step_long)
    else:
        locations = generate_locations_across_area(args.start_lat, args.start_long, args.end_lat, args.end_long)
    return locations


def _estimate_execution_time(locations_count, sleep_secs):
    return locations_count * sleep_secs * 1.1


def main():
    locations = get_locations_from_args()
    time_estimate = _estimate_execution_time(len(locations), args.sleep_secs)
    logging.info(f"Estimated execution time: "
                 f"{round(time_estimate, 2)} seconds --- "
                 f"{round(time_estimate/60, 2)} minutes --- "
                 f"{round(time_estimate/3600, 2)} hours")
    with open(args.search_params_file) as search_params_file:
        search_criteria = json.load(search_params_file)
    weighted_coordinates = assess_locations(locations, search_criteria, args.sleep_secs)
    heatmap = WeightedHeatmap(weighted_coordinates)
    logging.info("Generating heatmap...")
    heatmap.generate_weighted_heatmap(args.start_lat, args.end_long)


if __name__ == '__main__':
    args = parse_arguments()
    set_logging_level(args.log)
    main()
