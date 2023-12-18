# Standard library import
import argparse
import collections
import logging
import os

# Third party imports
import networkx as nx


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 10",
                                     description="Check https://adventofcode.com/2023/day/10 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    G = nx.Graph()
    animal_coordinates = []
    pipes = {'|', '-', 'L', 'J', '7', 'F', 'S'}
    possible_next_pipes = {0: {'|', 'L', 'J', 'S'},
                           1: {'-', '7', 'J', 'S'}}
    coordinates_to_node_id = collections.defaultdict(lambda : len(coordinates_to_node_id))
    with open(args.filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            for j, current_char in enumerate(line.strip()):
                if current_char == 'S':
                    animal_coordinates = (i,j)

                if not current_char in pipes:
                    continue

                neighbors = _get_next_neighbors(current_char, 
                                                (i, j), 
                                                lines, 
                                                possible_next_pipes)
                if not neighbors:
                    continue

                for neighbor in neighbors:
                    orig_node_id = coordinates_to_node_id[(i, j)]
                    dest_node_id = coordinates_to_node_id[neighbor]
                    G.add_edge(orig_node_id, dest_node_id)

    animal_node_id = coordinates_to_node_id[animal_coordinates]
    paths = list(nx.shortest_path(G, animal_node_id).values())
    print(len(paths[-1]) -1)


def _get_next_neighbors(current_char : str,
                        ij : tuple[int],
                        lines,
                        possible_next_pipes)->list[tuple[int]]:
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
        if next_neighbor_ij[0] >= len(lines):
            continue
        if next_neighbor_ij[1] >= len(lines[0].strip()):
            continue
        
        next_char = lines[next_neighbor_ij[0]][next_neighbor_ij[1]]
        if next_char in possible_next_pipes[next_direction]:
            neighbors.append(next_neighbor_ij)
 
    return neighbors
    

if __name__ == "__main__":
    main()