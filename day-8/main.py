# Standard library import
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 8",
                                     description="Check https://adventofcode.com/2023/day/8 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    with open(args.filename, 'r') as f:
        lines = f.readlines()

        initial_instructions=lines[0].strip()
        nb_instruction = len(initial_instructions)
        instructions_to_int={'L':0, 'R':1}
        
        nodes_to_next_nodes = {line [0:3]:(line[7:10], 
                                           line[12:15]) 
                                    for line in lines[2:]}
        
        current_node = 'AAA'
        nb_steps = 0
        while current_node != 'ZZZ':
            next_instruction = instructions_to_int[initial_instructions[nb_steps % nb_instruction]]
            current_node = nodes_to_next_nodes[current_node][next_instruction]
            nb_steps += 1
            
        print(f"nb_steps:{nb_steps}")   


if __name__ == "__main__":
    main()