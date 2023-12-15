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

    digits_as_words = ['one','two','three','four','five','six','seven','eight','nine']
    words_to_digits_dict = {word : i + 1 for i, word in enumerate(digits_as_words)}
    
    possible_digits = digits_as_words + list(words_to_digits_dict.values())

    total = 0
    with open(args.filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            first_nb = -1 
            first_nb_start = len(line)

            last_nb = -1
            last_nb_start = -1

            for possible_digit in possible_digits:
                for match in re.finditer(str(possible_digit), line):
                    if match.start() < first_nb_start:
                        first_nb_start = match.start()
                        first_nb = possible_digit if isinstance(possible_digit, int) else words_to_digits_dict[possible_digit]

                    if match.end() > last_nb_start:
                        last_nb_start = match.end()
                        last_nb = possible_digit if isinstance(possible_digit, int) else words_to_digits_dict[possible_digit]

            total += int(str(first_nb) + str(last_nb))
    
    print(total)


if __name__ == "__main__":
    main()