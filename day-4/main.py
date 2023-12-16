# Standard library import
import argparse
import collections
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
    total_part_2 = 0
    nb_card_per_index = collections.defaultdict(lambda: 0)
    with open(args.filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            current_card = i + 1
            nb_card_per_index[current_card] += 1

            all_cards = line.split(':')[1]
            eventual_winning_cards, cards_in_hand = [cards.split() for cards in all_cards.split('|')]
            winning_cards = list(set(eventual_winning_cards) & set(cards_in_hand))
            # Part 1
            if winning_cards:
                total_part_1 += pow(2, len(winning_cards) - 1)
            # Part 2
            nb_winning_cards = len(winning_cards)
            for next_card in range(current_card + 1, current_card + 1 + nb_winning_cards):
                nb_card_per_index[next_card] += nb_card_per_index[current_card]

    for number_card in nb_card_per_index.values():
        total_part_2 += number_card
        
    print(f"total_part_1:{total_part_1}")
    print(f"total_part_2:{total_part_2}")


if __name__ == "__main__":
    main()