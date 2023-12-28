# Standard library import
import argparse
import logging
import os

# Third party imports
import numpy as np
import networkx as nx

ALLOWED_STEP_IN_SAME_DIR = 3
NB_DIRECTIONS = 4

def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 17",
                                     description="Check https://adventofcode.com/2023/day/17 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    int_dir_to_dict = {0:'N', 1:'E', 2:'S', 3:'W'}
    next_node_dict = {0: (-1,  0), 
                      1: ( 0,  1), 
                      2: ( 1, -0), 
                      3: ( 0, -1)}
    G = nx.DiGraph()
    total_part_1 = 0
    with open(args.filename, 'r') as f:
        lines = f.read().split()
        matrix = np.matrix([list(map(int, list(line))) for line in lines])
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

                    # For each direction that is not going backward, split each node in 'ALLOWED_STEP_IN_SAME_DIR'
                    # nodes. Each node represent the number of steps still allowed to go in one direction. 
                    weight = matrix[next_node]
                    for step in range(1, ALLOWED_STEP_IN_SAME_DIR + 1):
                        current_node_id = f"{node}_{int_dir_to_dict[direction]}_{step}"
                        
                        prev_dir = (direction - 1) % NB_DIRECTIONS
                        next_node_id = f"{next_node}_{int_dir_to_dict[prev_dir]}_{ALLOWED_STEP_IN_SAME_DIR}"
                        G.add_edge(current_node_id, next_node_id, weight=weight)

                        next_dir = (direction + 1) % NB_DIRECTIONS
                        next_node_id = f"{next_node}_{int_dir_to_dict[next_dir]}_{ALLOWED_STEP_IN_SAME_DIR}"
                        G.add_edge(current_node_id, next_node_id, weight=weight)

                        if step - 1 > 0:
                            next_node_id = f"{next_node}_{int_dir_to_dict[direction]}_{step - 1}"
                            G.add_edge(current_node_id, next_node_id, weight=weight)
                            
    # Add links going from the first node to all its subnodes and all the subnodes of the last node to
    # the last node in order to compute shortest path
    start_node = f"{(0, 0)}"
    end_node = f"{(matrix.shape[0] - 1, matrix.shape[1] - 1)}"
    for direction in range(NB_DIRECTIONS):
        for step in range(1, ALLOWED_STEP_IN_SAME_DIR + 1):
            next_node_id = f"{start_node}_{int_dir_to_dict[direction]}_{step}"
            G.add_edge(start_node, next_node_id)

            prev_node_id = f"{end_node}_{int_dir_to_dict[direction]}_{step}"
            G.add_edge(prev_node_id, end_node)
        
    path = nx.shortest_path(G, start_node, end_node, weight='weight')
    for node in path[2:-1]:
        total_part_1 += matrix[eval(node.split('_')[0])]
    print(f"total_part_1:{total_part_1}")
    

if __name__ == "__main__":
    main()