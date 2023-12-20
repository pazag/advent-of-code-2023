# Standard library import
import argparse
import collections
import logging
import os

# Third party import
import numpy as np


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 14",
                                     description="Check https://adventofcode.com/2023/day/14 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    total_part_1 = 0
    with open(args.filename, 'r') as f:
        lines = f.read().split()
        char_matrix = np.matrix([list(line) for line in lines])
        for j in range(char_matrix.shape[1]):
            last_possible_rock_row = 0
            for i in range(char_matrix.shape[0]):
                if char_matrix[i,j] == '#':
                    last_possible_rock_row = i + 1
                elif char_matrix[i,j] == 'O':
                    total_part_1 += char_matrix.shape[0] - last_possible_rock_row
                    last_possible_rock_row += 1        
    print(total_part_1)


if __name__ == "__main__":
    main()