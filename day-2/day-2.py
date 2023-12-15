# Standard library import
import argparse
import logging
import os
import re


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 2",
                                     description="Check https://adventofcode.com/2023/day/2 \
                                                  to see the problem solved by this script.")
    parser.add_argument("games", help="File containing the games.")
    parser.add_argument("cubes", help="File containing the cubes.")

    args = parser.parse_args()
    if not os.path.exists(args.games):
        logging.error(f"File '{args.games}' does not exist.")

    if not os.path.exists(args.cubes):
        logging.error(f"File '{args.cubes}' does not exist.")

    available_cubes = {}
    with open(args.cubes, 'r') as f:
        lines = f.readlines()
        available_cubes = get_cubes(lines[0])

    total = 0
    with open(args.games, 'r') as f:
        lines = f.readlines()
        for line in lines:
            game_with_id, concatenated_games = line.split(":")
            game_id = int(game_with_id.split("Game ")[1])

            max_cubes_per_game = get_cubes(concatenated_games)

            is_valid = True
            for color, nb_cube in available_cubes.items():
                if nb_cube < max_cubes_per_game[color]:
                    is_valid = False
            if is_valid:
                total += game_id
    print(total)


def get_cubes(concatenated_games: str):
    """ 
    Given a list of games, return the maximum number of cubes needed for each color as 
    a tuple (R,G,B) of int.
    """
    cubes = {"red" : 0, "green" : 0, "blue" : 0}
    games_as_txt = concatenated_games.split(";")
    for game_as_txt in games_as_txt:
        for nb_and_color in game_as_txt.split(','):
            nb, color  = nb_and_color.split()
            cubes[color] = max(int(nb), cubes[color])
    return cubes



if __name__ == "__main__":
    main()