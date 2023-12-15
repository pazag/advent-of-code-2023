# Standard library import
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 4",
                                     description="Check https://adventofcode.com/2023/day/4 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    total_part_1 = 0
    with open(args.filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            all_cards = line.split(':')[1]
            eventual_winning_cards, cards_in_hand = [cards.split() for cards in all_cards.split('|')]
            winning_cards = list(set(eventual_winning_cards) & set(cards_in_hand))
            if winning_cards:
                total_part_1 += pow(2, len(winning_cards) - 1)
    print(total_part_1)


if __name__ == "__main__":
    main()