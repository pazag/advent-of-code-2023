# Standard library import
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 12",
                                     description="Check https://adventofcode.com/2023/day/12 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    total_part_1 = 0
    with open(args.filename, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            records, arrangement = line.split()
            arrangement = [int(group_length) for group_length in arrangement.split(',')]
            total_part_1 += _number_of_arrangements(records, arrangement)
    print(f"total_part_1:{total_part_1}")


def _number_of_arrangements(record : str, 
                            arrangement : list[int]):
    if not record:
        return 0 if arrangement else 1
    
    current_char = record[0]
    if current_char == '.':
        return _number_of_arrangements(record[1:], arrangement)
    if current_char == '?':
        return _number_of_arrangements('.' + record[1:], arrangement) + \
               _number_of_arrangements('#' + record[1:], arrangement)
    if current_char == '#':
        if not arrangement:
            return 0
        i = 0
        while i < len(record) and record[i] == '#':
            i += 1

        if i < len(record) and record[i] == '?':
            hashtags = '#' * i
            return _number_of_arrangements(hashtags + '#' + record[i + 1:], arrangement) + \
                   _number_of_arrangements(hashtags + '.' + record[i + 1:], arrangement)
        else:
            arrangement_copy = arrangement.copy()
            sub_group_size = arrangement_copy.pop(0)
            if i != sub_group_size:
                return 0
            else:
                return _number_of_arrangements(record[i + 1:], arrangement_copy)

    logging.error(f"Exited function without returning number.")  


if __name__ == "__main__":
    main()