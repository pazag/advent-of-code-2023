# Standard library import
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 3",
                                     description="Check https://adventofcode.com/2023/day/3 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")

    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    total = 0
    with open(args.filename, 'r') as f:
        lines = f.readlines()
        number_start = -1
        number_end = -1
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
                    # Validate if it is a 'part number'
                    has_a_symbol_neighbor = False
                    neighbor_coordinates = _neighbors_coordinates(number_start, 
                                                                  number_end, 
                                                                  line_idx, 
                                                                  lines)
                    for neighbor_coordinates in neighbor_coordinates:
                        neighbor = lines[neighbor_coordinates[0]][neighbor_coordinates[1]]
                        if not neighbor.isdigit() and neighbor != '.':
                            has_a_symbol_neighbor = True
                            break

                    if has_a_symbol_neighbor:
                        total += int(line[number_start:number_end + 1])

                    # Reset number delimitors
                    number_start, number_end = -1, -1
    print(total)


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