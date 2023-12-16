# Standard library import
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 9",
                                     description="Check https://adventofcode.com/2023/day/9 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    with open(args.filename, 'r') as f:
        lines = f.readlines()
        histories = []
        for line in lines:
            histories.append(list(map(int, line.split())))

        total_part_1 = 0
        total_part_2 = 0

        for history in histories:
            # Fill from top to bottom
            history_sequences = [history.copy()]
            while not all(sequence == 0 for sequence in history_sequences[-1]):
                sequence = []
                previous_sequence = history_sequences[-1]
                for i in range(len(previous_sequence) - 1):
                    sequence.append(previous_sequence[i + 1] - previous_sequence[i])
                history_sequences.append(sequence.copy())

            # Compute results from bottom to top
            # Part 1 
            history_top_value = _get_history_top_value(history_sequences, False)
            total_part_1 += history_top_value
            
            # Part 2
            history_top_value = _get_history_top_value(history_sequences, True)
            total_part_2 += history_top_value

        print(f"total_part_1:{total_part_1}")
        print(f"total_part_2:{total_part_2}")


def _get_history_top_value(history_sequences : list[list[int]],
                           is_part_2: bool):
    '''
    Complete the history sequences starting from the bottom. Return the last value
    of the first sequence (False) or the first value of the first sequence (True) 
    depending on the value of the parameter "is_part_2".
    '''
    history_sequences[-1].append(0)
    nb_histories = len(history_sequences)
    for i in range(1, len(history_sequences)):
        top_story    = history_sequences[nb_histories - i - 1]
        bottom_story = history_sequences[nb_histories - i]
        if is_part_2:
            top_story.insert(0, top_story[0] - bottom_story[0])
        else:
            top_story.append(top_story[-1] + bottom_story[-1])
    
    return history_sequences[0][0] if is_part_2 else history_sequences[0][-1]


if __name__ == "__main__":
    main()