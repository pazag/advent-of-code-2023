# Standard library import
import argparse
import logging
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
        times = [int(time) for time in lines[0].split(':')[1].split()]
        distances = [int(distance) for distance in lines[1].split(':')[1].split()]
        
        total = 1
        for time, distance in zip(times, distances):
            better_distances = []
            for acceleration_time in range(time):
                possible_distance = (time - acceleration_time) * acceleration_time 
                if possible_distance > distance:
                    better_distances.append(possible_distance)
            total *= len(better_distances)
        print(total)


if __name__ == "__main__":
    main()