# Standard library import
import argparse
import logging
import os

# Third party imports
import numpy as np
import networkx as nx


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 17",
                                     description="Check https://adventofcode.com/2023/day/17 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    with open(args.filename, 'r') as f:
        lines = f.read().split()
        matrix = np.matrix([list(map(int, list(line))) for line in lines])
        print(f"total_part_1:{_shortest_path_weight(matrix, 3, 0)}")
        print(f"total_part_2:{_shortest_path_weight(matrix, 10, 4)}")
    

def _shortest_path_weight(matrix, 
                          nb_allowed_step, 
                          minimal_step_before_turning_direction):
    NB_DIRECTIONS = 4
    int_dir_to_dict = {0:'N', 1:'E', 2:'S', 3:'W'}
    next_node_dict = {0: (-1,  0), 
                      1: ( 0,  1), 
                      2: ( 1, -0), 
                      3: ( 0, -1)}
    G = nx.DiGraph()
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            node = (i,j)
            # Split each node in 4 nodes for each direction
            for direction in range(NB_DIRECTIONS):
                next_node = tuple(map(lambda i,j : i + j, node, next_node_dict[direction]))
                # No need to create edges if next node is not inside the matrix
                if 0 > next_node[0] or next_node[0] > matrix.shape[0] - 1:
                    continue
                if 0 > next_node[1] or next_node[1] > matrix.shape[1] - 1:
                    continue
                weight = matrix[next_node]
                # For each direction that is not going backward, split each "sub-node" 
                # in 'nb_allowed_step' nodes. Each node represent the number of steps still allowed to go 
                # in one direction. 
                for nb_step_done in range(nb_allowed_step):
                    current_node_id = f"{node}_{int_dir_to_dict[direction]}_{nb_step_done}"
                    if nb_step_done + 1 >= minimal_step_before_turning_direction:
                        prev_dir = (direction - 1) % NB_DIRECTIONS
                        next_node_id = f"{next_node}_{int_dir_to_dict[prev_dir]}_{0}"
                        G.add_edge(current_node_id, next_node_id, weight=weight)

                        next_dir = (direction + 1) % NB_DIRECTIONS
                        next_node_id = f"{next_node}_{int_dir_to_dict[next_dir]}_{0}"
                        G.add_edge(current_node_id, next_node_id, weight=weight)

                    if nb_step_done < nb_allowed_step:
                        next_node_id = f"{next_node}_{int_dir_to_dict[direction]}_{nb_step_done + 1}"
                        G.add_edge(current_node_id, next_node_id, weight=weight)

    # Add links going from the first node to all its possible subnodes and from all the subnodes 
    # that are at least 'minimal_step_before_turning_direction' from the last node to the last node.
    start_node = f"{(0, 0)}"
    end_node = f"{(matrix.shape[0] - 1, matrix.shape[1] - 1)}"
    for direction in range(NB_DIRECTIONS):
        next_node_id = f"{start_node}_{int_dir_to_dict[direction]}_{0}"
        G.add_edge(start_node, next_node_id, weight=0)
        for nb_step_done in range(nb_allowed_step + 1):
            if nb_step_done >= minimal_step_before_turning_direction:
                prev_node_id = f"{end_node}_{int_dir_to_dict[direction]}_{nb_step_done}"
                G.add_edge(prev_node_id, end_node, weight=0)

    # Ignore the two first nodes since we start on the top corner and second end node since it is
    # a copy of the end node
    path_weight = 0
    path = nx.shortest_path(G, start_node, end_node, weight='weight')
    for node in path[2:-1]:
        path_weight += matrix[eval(node.split('_')[0])]
    return path_weight
    

if __name__ == "__main__":
    main()