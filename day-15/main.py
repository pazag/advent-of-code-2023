# Standard library import
import argparse
import collections
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 15",
                                     description="Check https://adventofcode.com/2023/day/15 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    total_part_1 = 0
    total_part_2 = 0
    with open(args.filename, 'r') as f:
        lines = f.read().split()
        strings = lines[0].split(',')
        hashmap = collections.defaultdict(lambda:[])
        for string in strings:
            # Part 1 
            total_part_1 += _hash(string)
            
            # Part 2
            n = 0
            while string[n] != '=' and string[n] != '-':
                n += 1
            lens = string[:n]   
            box = _hash(lens)
            if string[n] == '-':
                for i, lens_focal in enumerate(hashmap[box]):
                    if lens == lens_focal[0]:
                        hashmap[box].pop(i)
            else:
                focal = int(string[n + 1])
                lens_in_hashmap = False
                for i, lens_focal in enumerate(hashmap[box]):
                    if lens == lens_focal[0]:
                        hashmap[box][i] = (lens, focal)
                        lens_in_hashmap = True
                        break
                if not lens_in_hashmap:
                    hashmap[box].append((lens, focal))
        for box, lens_focal_list in hashmap.items():
            for i, lens_focal in enumerate(lens_focal_list):
                total_part_2 += (box + 1) * (i + 1) * lens_focal[1]
    print(f"total_part_1:{total_part_1}")
    print(f"total_part_2:{total_part_2}")


def _hash(string):
    hash_value = 0
    for char in string:
        hash_value += ord(char)
        hash_value *= 17
        hash_value = hash_value % 256 
    return hash_value


if __name__ == "__main__":
    main()