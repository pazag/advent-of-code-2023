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
    seeds_groups_part_1 = []
    seeds_groups_part_2 = []

    with open(args.filename, 'r') as f:
        lines = f.readlines()
        # 1 - Get seeds first to have the same parsing loop after
        # Part 1 
        for seed in lines[0].split(':')[1].split():
            seeds_groups_part_1.append([int(seed), int(seed)])

        # Part 2 
        for i in range(0, len(seeds_groups_part_1), 2):
            seeds_groups_part_2.append([seeds_groups_part_1[i][0], 
                                        seeds_groups_part_1[i][0] + seeds_groups_part_1[i+1][0] - 1])
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
    _get_min_path(seeds_groups_part_1, almanac_map)

    print("------Part 2------")
    _get_min_path(seeds_groups_part_2, almanac_map)


def _get_intersection(interval_1 : list[int], 
                      interval_2 : list[int])->list[int]:
    """ 
    Returns the intersection of two intervals.
    """
    new_min = max(interval_1[0], interval_2[0])
    new_max = min(interval_1[1], interval_2[1])
    if new_min > new_max:
        return []
    else:
        return [new_min, new_max]


def _new_path(path : list[list[int]], 
              filtered_current_group : list[int],
              next_group: list[int])->list[int]:
    ''' 
    Returns a new path. It may also reduce the size of all previous groups using 
    the "filtered_current_group" since this group may be a subset of the last element
    of the group (before adding a new one). 
    '''
    new_path = path.copy()
    lower_delta = new_path[-1][0] - filtered_current_group[0]
    upper_delta = new_path[-1][1] - filtered_current_group[1]
    new_path = [[group[0] - lower_delta , 
                 group[1] - upper_delta] for group in new_path]
    new_path.append(next_group)
    return new_path


def _get_min_path(seeds_groups : list[list[int]],
                  almanac_map : dict[str, int]):
    '''
    For each seeds groups, compute the path to their respective location using the 
    "almanac_map". After computing those paths, it will return the path with the lowest 
    location number (end of path).
    '''
    new_paths = [[seeds_group] for seeds_group in seeds_groups]
    for source_to_dest_map in almanac_map.values():
        paths = new_paths
        new_paths = []

        for path in paths:
            current_group = path[-1]
            intersections = []
            # Determine existing groups
            for source_interval, destination_interval in source_to_dest_map.items():
                intersection = _get_intersection(source_interval, 
                                                 current_group)
                if intersection:
                    lower_bound = intersection[0] - source_interval[0] + destination_interval[0]
                    next_group = [lower_bound,
                                  lower_bound + intersection[1] - intersection[0]]
                    new_paths.append(_new_path(path,
                                               intersection, 
                                               next_group))
                    intersections.append(intersection)
            
            # Intersections must be sorted in order not to add several times the same interval.
            intersections.sort()
            i = current_group[0]
            while i <= current_group[1]:
                if intersections:
                    intersection = intersections.pop(0)
                    if i < intersection[0]:
                        new_paths.append(_new_path(path, 
                                                   [i, intersection[0] - 1],
                                                   [i, intersection[0] - 1]))
                    i = intersection[1] + 1
                else:
                    new_paths.append(_new_path(path,
                                               [i, current_group[1]],
                                               [i, current_group[1]]))
                    break

    min_path = min(new_paths, key=lambda x:x[-1][0])
    print("---Solution---")
    print(f"min_path:{min_path}")
    print(f"min_location:{min_path[-1][0]}")
  

if __name__ == "__main__":
    main()