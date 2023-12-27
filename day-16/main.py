# Standard library import
import argparse
import collections
import logging
import os
import sys

# Third party imports
import numpy as np

def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 16",
                                     description="Check https://adventofcode.com/2023/day/16 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    total_part_1 = 0
    with open(args.filename, 'r') as f:
        lines = f.read().split()
        char_matrix = np.matrix([list(line) for line in lines])
        sys.setrecursionlimit(char_matrix.shape[0] * char_matrix.shape[1])
        
        # Part 1
        visited = collections.defaultdict(lambda:set())
        _continue_ray(visited, char_matrix, (0,0), 'E')
        total_part_1 = len(visited)

        # Part 2
        total_part_2 = 0
        nb_rows, nb_columns = char_matrix.shape
        for i in range(nb_rows):
            for j in range(nb_columns):
                next_directions = []
                if i == 0:
                    next_directions.append('S')
                elif i == nb_rows - 1:
                    next_directions.append('N')
                elif j == 0:
                    next_directions.append('E')
                elif j == nb_columns - 1:
                    next_directions.append('W')

                for next_direction in next_directions:
                    visited = collections.defaultdict(lambda:set())
                    _continue_ray(visited, char_matrix, (i,j), next_direction)
                    total_part_2 = max(len(visited), total_part_2)

    print(f"total_part_1:{total_part_1}")
    print(f"total_part_2:{total_part_2}")

def _continue_ray(visited : dict[tuple[int], set[str]], 
                  char_matrix : np.matrix, 
                  node : tuple[int],
                  coming_from : str):
    if _is_outside_matrix(node, char_matrix):
        return

    if coming_from in visited[node]:
        return

    next_dir_dict = {'N' : {'.' : ['N'],
                            '|' : ['N'],
                            '-' : ['E', 'W'],
                            '/' : ['E'],
                            '\\' : ['W']},
                     'E' : {'.' : ['E'],
                            '|' : ['N', 'S'],
                            '-' : ['E'],
                            '/' : ['N'],
                            '\\' : ['S']},
                     'S' : {'.' : ['S'],
                            '|' : ['S'],
                            '-' : ['E', 'W'],
                            '/' : ['W'],
                            '\\' : ['E']},
                     'W' : {'.' : ['W'],
                            '|' : ['N', 'S'],
                            '-' : ['W'],
                            '/' : ['S'],
                            '\\' : ['N']}}
    
    # Remember visited nodes and opposite direction for '.' in order to have less iterations
    visited[node].add(coming_from)
    current_char = char_matrix[node]
    if current_char == '.':
        opposite_dir_dict = {'N' : 'S', 'E' : 'W', 'S' : 'N', 'W' : 'E'}
        visited[node].add(opposite_dir_dict[coming_from])
    
    for next_dir in next_dir_dict[coming_from][current_char]:
        next_node = _get_next_node(node, next_dir)
        _continue_ray(visited, char_matrix, next_node, next_dir)

def _get_next_node(node, direction):
    match direction:
        case 'N':
            return (node[0] - 1, node[1])
        case 'E':
            return (node[0], node[1] + 1)
        case 'S':
            return (node[0] + 1, node[1])
        case 'W':
            return (node[0], node[1] - 1)

def _is_outside_matrix(ij, char_matrix):
    i, j = ij
    if i >= np.shape(char_matrix)[0] or i < 0:
        return True
    if j >= np.shape(char_matrix)[1] or j < 0:
        return True
    return False

if __name__ == "__main__":
    main()