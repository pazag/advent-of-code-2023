# Standard library import
import argparse
import logging
import os

# Third party import
import numpy as np


NB_CYCLE = 1000000000


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 14",
                                     description="Check https://adventofcode.com/2023/day/14 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    total_part_1 = 0
    total_part_2 = 0
    with open(args.filename, 'r') as f:
        lines = f.read().split()
        char_matrix = np.matrix([list(line) for line in lines])
        # Part 1
        char_matrix_part_1 = _move_rocks_to_top(char_matrix)
        total_part_1 += _calculate_load(char_matrix_part_1)
        print(f"total_part_1:{total_part_1}")


        # Part 2 (Does not scale)
        for n in range(NB_CYCLE):
            for i in range(4):
                char_matrix = _move_rocks_to_top(char_matrix)
                char_matrix = np.rot90(char_matrix, k=1, axes=(1,0))
        total_part_2 += _calculate_load(char_matrix)
        print(f"total_part_2:{total_part_2}")


def _move_rocks_to_top(matrix)->np.matrix:
    for j in range(matrix.shape[1]):
        last_possible_rock_row = 0
        for i in range(matrix.shape[0]):
            ij = (i,j)
            if matrix[ij] == '#':
                last_possible_rock_row = i + 1
            elif matrix[ij] == 'O':
                matrix[last_possible_rock_row, j] = 'O'
                if not i == last_possible_rock_row:
                    matrix[ij] = '.'
                last_possible_rock_row += 1
    return matrix


def _calculate_load(matrix):
    print(matrix)
    load = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i,j] == 'O':
                load += matrix.shape[0] - i
    return load


if __name__ == "__main__":
    main()