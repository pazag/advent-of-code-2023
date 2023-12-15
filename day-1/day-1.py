# Standard library import
import argparse
import logging
import os
import re


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 1",
                                     description="Given a file, it will print the sum of the     \
                                                  concatenation of the first digit of the line   \
                                                  and the last digit of the line. If no digit is \
                                                  found in the line, nothing will be added for   \
                                                  line.")
    parser.add_argument("filename", help="File to parse")

    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File '{args.filename}' does not exist.")

    total = 0
    with open(args.filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            number_list = re.findall(r'\d+', line)
            if not number_list:
                logging.error(f"No number were found in line '{line}'")
            total += int(number_list[0][0] + number_list[-1][-1])
    
    print(total)


if __name__ == "__main__":
    main()