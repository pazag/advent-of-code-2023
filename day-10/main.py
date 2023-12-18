# Standard library import
import argparse
import collections
import logging
import os

# Third party imports
import networkx as nx
import numpy as np

def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 10",
                                     description="Check https://adventofcode.com/2023/day/10 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    G = nx.Graph()
    animal_coordinates = None
    pipes = {'|', '-', 'L', 'J', '7', 'F', 'S'}
    coordinates_to_node_id = collections.defaultdict(lambda : len(coordinates_to_node_id))
    with open(args.filename, 'r') as f:
        lines = f.read().split()
        char_matrix = np.matrix([list(line) for line in lines])
        nb_line, nb_column = np.shape(char_matrix)
        for i in range(nb_line):
            for j in range(nb_column):
                ij = (i,j)
                current_char = char_matrix[ij]
                if current_char == 'S':
                    animal_coordinates = ij

                if not current_char in pipes:
                    continue

                neighbors = _get_next_neighbors(current_char, ij, char_matrix)
                if not neighbors:
                    continue

                for neighbor in neighbors:
                    G.add_edge(ij, neighbor)

    paths = list(nx.shortest_path(G, animal_coordinates).values())
    print(len(paths[-1]) -1)


def _get_next_neighbors(current_char : str,
                        ij : tuple[int],
                        char_matrix)->list[tuple[int]]:
    
    # 0 : Next vertical neighbor
    # 1 : Next horizontal neighbor
    possible_next_pipes = {0: {'|', 'L', 'J', 'S'},
                           1: {'-', '7', 'J', 'S'}}
    next_neighbor_ij_list = [None, None]
    match current_char:
        case '|' | '7':
            next_neighbor_ij_list[0] = (ij[0] + 1, ij[1])
        case '-' | 'L':
            next_neighbor_ij_list[1] = (ij[0], ij[1] + 1)
        case 'F' | 'S':
            next_neighbor_ij_list[0] = (ij[0] + 1, ij[1])
            next_neighbor_ij_list[1] = (ij[0], ij[1] + 1)
        case _:
            return None

    neighbors = []
    for next_direction, next_neighbor_ij in enumerate(next_neighbor_ij_list):
        if not next_neighbor_ij:
            continue
        if _is_outside_matrix(next_neighbor_ij, char_matrix):
            continue
        
        next_char = char_matrix[next_neighbor_ij]
        if next_char in possible_next_pipes[next_direction]:
            neighbors.append(next_neighbor_ij)
 
    return neighbors
    

def _is_outside_matrix(ij, char_matrix):
    i, j = ij
    if i >= np.shape(char_matrix)[0]:
        return True
    if j >= np.shape(char_matrix)[1]:
        return True
    return False


if __name__ == "__main__":
    main()