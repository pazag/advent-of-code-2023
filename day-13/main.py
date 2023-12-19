# Standard library import
import argparse
import logging
import os

# Third party import
import numpy as np


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 13",
                                     description="Check https://adventofcode.com/2023/day/13 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    total_part_1 = 0
    patterns = []
    with open(args.filename, 'r') as f:
        lines = f.read().split('\n')
        pattern_start = 0
        for i, line in enumerate(lines):
            if not line:
                patterns.append(np.matrix([list(line) for line in lines[pattern_start:i]]))
                pattern_start = i + 1
    
    for pattern in patterns:
        total_part_1 += _rows_above_horizontal_mirrors(pattern, True) * 100
        total_part_1 += _rows_above_horizontal_mirrors(pattern, False) 
    print(f"total_part_1:{total_part_1}")


def _rows_above_horizontal_mirrors(matrix, 
                                   iterate_over_rows):
    nb_line_next_to_mirror = 0
    N = matrix.shape[0] if iterate_over_rows else matrix.shape[1]
    for n in range(N - 1):
        array_1 = matrix[n] if iterate_over_rows else matrix[:, n]
        array_2 = matrix[n + 1] if iterate_over_rows else matrix[:, n + 1]
        if _identical_arrays(array_1, array_2):
            is_mirror = False
            for m in range(1, N):
                if n - m < 0 or n + 1 + m >= N:
                    is_mirror = True
                    break
                array_1 = matrix[n     - m] if iterate_over_rows else matrix[:, n     - m]
                array_2 = matrix[n + 1 + m] if iterate_over_rows else matrix[:, n + 1 + m]
                if not _identical_arrays(array_1, array_2):
                    break
            if is_mirror:
                nb_line_next_to_mirror += n + 1
    return nb_line_next_to_mirror


def _identical_arrays(array_1,
                      array_2):
    if array_1.shape != array_2.shape:
        return False
    
    for i in range(array_1.shape[0]):
        for j in range(array_1.shape[1]):
            if array_1[i,j] != array_2[i,j]:
                return False
    return True


if __name__ == "__main__":
    main()