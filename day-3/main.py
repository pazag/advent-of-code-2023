# Standard library import
import argparse
import logging
import os
import collections

# Third library import
import numpy as np

def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 3",
                                     description="Check https://adventofcode.com/2023/day/3 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")

    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    total_part_1 = 0

    neigh_of_symbol_coordinates_dict = collections.defaultdict(lambda: [])
    # This dictionary is defined as followed (for part 2 only):
    #   - Keys are the coordinates (i,j) of the symbol
    #   - Values are the part numbers that are neighbors of this symbol 
    
    with open(args.filename, 'r') as f:
        lines = f.readlines()

        number_start, number_end = -1, -1
        for line_idx, line in enumerate(lines):
            for character_idx, character in enumerate(line):
                # Find number extremities
                if number_start == -1 and character.isdigit():
                    number_start = character_idx

                if number_start != -1:
                    if character_idx == len(line) - 1:
                        number_end = character_idx
                    elif not character.isdigit():
                        number_end = character_idx -1

                if number_start != -1 and number_end != -1:
                    neighbor_coordinates = _neighbors_coordinates(number_start, 
                                                                  number_end, 
                                                                  line_idx, 
                                                                  lines)
                    
                    is_part_number = False
                    current_number = int(line[number_start:number_end + 1])

                    for neighbor_coordinates in neighbor_coordinates:
                        neighbor = lines[neighbor_coordinates[0]][neighbor_coordinates[1]]
                        if not neighbor.isdigit() and neighbor != '.':
                            # Part 1
                            is_part_number = True
                            # Part 2
                            neigh_of_symbol_coordinates_dict[neighbor_coordinates].append(current_number)

                    if is_part_number:
                        total_part_1 += current_number

                    # Reset number delimitors
                    number_start, number_end = -1, -1
    
    total_part_2 = sum([np.prod(part_numbers) for part_numbers in neigh_of_symbol_coordinates_dict.values() 
                                                   if len(part_numbers) == 2]) 
    print(f"total_part_1:{total_part_1}")
    print(f"total_part_2:{total_part_2}")


def _neighbors_coordinates(number_start:int,
                           number_end:int,
                           current_line:int,
                           lines:list[str])->list[tuple[int]]:
    ''' 
    Return a list containing the coordinates of the neighbors of the number which is on line
    "current_line" and that is delimited by "number_start" and "number_end".
    '''
    # We assume that the file contains a square schematic
    nb_line = len(lines)
    return [(i, j) for i in range (current_line - 1, current_line + 2)
                   for j in range (number_start - 1, number_end + 2)
                   if (-1 < i < nb_line and
                       -1 < j < nb_line and
                       (i != current_line or j < number_start or j > number_end))]


if __name__ == "__main__":
    main()