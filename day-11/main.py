# Standard library import
import argparse
import logging
import os

# Third party imports
import numpy as np

EMPTY_ROWS_TO_ADD    = 1000000 - 1
EMPTY_COLUMNS_TO_ADD = 1000000 - 1


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 11",
                                     description="Check https://adventofcode.com/2023/day/11 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    # 1 - Get galaxies coordinates
    galaxies_part_1 = set()
    galaxies_part_2 = set()
    with open(args.filename, 'r') as f:
        lines = f.read().split()

        char_matrix = np.matrix([list(line) for line in lines])
        nb_line, nb_column = np.shape(char_matrix)
        row_with_galaxies = np.any(char_matrix == '#', axis=1)        
        column_with_galaxies = np.any(char_matrix == '#', axis=0)
        
        added_row = 0
        for i in range(nb_line):
            added_column = 0
            if not row_with_galaxies[i][0]:
                added_row += EMPTY_ROWS_TO_ADD
                continue
            for j in range(nb_column):
                if not column_with_galaxies[(0,j)]:
                    added_column += EMPTY_COLUMNS_TO_ADD
                    continue

                if char_matrix[(i,j)] == '.':
                    continue
                
                galaxies_part_1.add((i + added_row // EMPTY_ROWS_TO_ADD, 
                                     j + added_column // EMPTY_COLUMNS_TO_ADD))
                galaxies_part_2.add((i + added_row, 
                                     j + added_column))
    # 2 - Compute results
    total_part_1 = _get_total_distance_between_galaxies(galaxies_part_1)
    print(f"total_part_1:{total_part_1}")

    total_part_2 = _get_total_distance_between_galaxies(galaxies_part_2)
    print(f"total_part_2:{total_part_2}")

    
def _get_total_distance_between_galaxies(galaxies):
    total = 0
    for galaxy in galaxies:
        for galaxy_2 in galaxies:
            if galaxy >= galaxy_2:
                continue
            total += abs(galaxy[0] - galaxy_2[0]) + abs(galaxy[1] - galaxy_2[1])
    return total


if __name__ == "__main__":
    main()