# Standard library import
import argparse
import collections
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 5",
                                     description="Check https://adventofcode.com/2023/day/5 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    # Dictionary containing all the corresponding maps
    almanac_map = collections.defaultdict(lambda: {})
    seeds_part_1 = []

    with open(args.filename, 'r') as f:
        lines = f.readlines()
        # 1 - Get seeds first to have the same parsing loop after
        for seed in lines[0].split(':')[1].split():
            seeds_part_1.append(int(seed))

        # 2 - Parse the map for each category
        category = '' 
        for line in lines[2:]:
            if not line.rstrip():
                continue

            if not line[0].isdigit():
                category = line.split(':')[0]
                continue

            destination, source, number = map(lambda x:int(x), line.split())
            almanac_map[category][(source, source + number - 1)] = (destination, destination + number - 1)

    # Compute results
    print("------Part 1------")
    _get_min_path(seeds_part_1, almanac_map)


def _get_min_path(seeds : list[list[int]],
                  almanac_map : dict[str, int]):
    '''
    For each seed, compute the path to its location using the "almanac_map". After computing
    those paths, it will return the path with the lowest location number (end of path).
    '''
    new_paths = [[seed] for seed in seeds]
    for source_to_dest_map in almanac_map.values():
        paths = new_paths
        new_paths = []

        for path in paths:
            current_node = path[-1]
            has_found_next_node = False
            for source_interval, destination_interval in source_to_dest_map.items():
                if source_interval[0] <= current_node <= source_interval[1]:
                    next_node = current_node - source_interval[0] + destination_interval[0]
                    new_paths.append(path + [next_node])
                    has_found_next_node = True
                    break

            if not has_found_next_node:
                new_paths.append(path + [current_node])

    min_path = min(new_paths, key=lambda x:x[-1])
    print("---Solution---")
    print(f"min_path:{min_path}")
    print(f"min_location:{min_path[-1]}")
  

if __name__ == "__main__":
    main()