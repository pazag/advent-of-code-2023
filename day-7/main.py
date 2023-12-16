# Standard library import
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 7",
                                     description="Check https://adventofcode.com/2023/day/7 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    card_strenght_order = ['A', 'K', 'Q', 'J', 'T'] 
    for i in range(9, 1, -1):
        card_strenght_order.append(str(i))
    card_strenght_order = {card:(len(card_strenght_order)-strenght) for (strenght, card) in enumerate(card_strenght_order)}

    with open(args.filename, 'r') as f:
        lines = f.readlines()
        cards_and_bid_list = []
        for line in lines:
            cards_in_hand, bid = line.split()
            cards_as_list = sorted(cards_in_hand)
            cards_as_list.sort(key=lambda x:(cards_in_hand.count(x), 
                                             card_strenght_order[x]))
            sorted_cards_in_hand = ''.join(cards_as_list)
            # For each hand, keep the triplet (sorted cards, bid, initial cards) so that the
            # different hands are easier to sort
            cards_and_bid_list.append([sorted_cards_in_hand, int(bid), cards_in_hand])

        # First and second criteria can sort the different type of hands:
        #     High card < One Pair < Two pair < Three of a kind < Full house < Four of a kind < Five of a kind
        # Third to last criteria are used to rank two hands of similar types based on the value of the cards.
        cards_and_bid_list.sort(key=lambda cards_and_bid:(cards_and_bid[0].count(cards_and_bid[0][4]),
                                                          cards_and_bid[0].count(cards_and_bid[0][1]),
                                                          card_strenght_order[cards_and_bid[2][0]],
                                                          card_strenght_order[cards_and_bid[2][1]],
                                                          card_strenght_order[cards_and_bid[2][2]],
                                                          card_strenght_order[cards_and_bid[2][3]],
                                                          card_strenght_order[cards_and_bid[2][4]]))
        total = 0
        for i in range(len(cards_and_bid_list)):
            total += cards_and_bid_list[i][1] * (i + 1) 
        print(total)        


if __name__ == "__main__":
    main()