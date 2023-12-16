# Standard library import
import argparse
import logging
import math
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 6",
                                     description="Check https://adventofcode.com/2023/day/6 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    with open(args.filename, 'r') as f:
        lines = f.readlines()
        time_line = [time for time in lines[0].split(':')[1].split()]
        distance_line = [distance for distance in lines[1].split(':')[1].split()]
        
        # Part 1 
        times = [int(time) for time in time_line]
        distances = [int(distance) for distance in distance_line]

        total_part_1 = 1
        for time, distance in zip(times, distances):
            better_distances = []
            for acceleration_time in range(time):
                possible_distance = (time - acceleration_time) * acceleration_time 
                if possible_distance > distance:
                    better_distances.append(possible_distance)
            total_part_1 *= len(better_distances)
        print(f"total_part_1:{total_part_1}")

        # Part 2 
        max_time = int(''.join(time_line))
        min_distance = int(''.join(distance_line))
        # We are looking for the interval for which this function is positive:
        #   f:t -> (max_time - t) * t - min_distance
        delta = max_time*max_time - 4 * (-1) * (-min_distance)
        roots = [(-max_time - math.sqrt(delta))/(2*(-1)), 
                 (-max_time + math.sqrt(delta))/(2*(-1))]
        roots.sort()
        bounds = [max(0, math.ceil(roots[0])),
                  min(max_time, math.floor(roots[1]))]
        print(f"total_part_2:{bounds[1] - bounds[0] + 1}")


if __name__ == "__main__":
    main()