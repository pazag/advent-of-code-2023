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
    with open(args.filename, 'r') as f:
        lines = f.read().split()
        char_matrix = np.matrix([list(line) for line in lines])
        nb_line, nb_column = np.shape(char_matrix)
        for i in range(nb_line):
            for j in range(nb_column):
                ij = (i,j)
                G.add_node(ij)
                current_char = char_matrix[ij]
                if current_char == 'S':
                    animal_coordinates = ij

                if not current_char in pipes:
                    neighbors = [(i + 1, j), (i, j + 1)]
                    for neighbor in neighbors:
                        if not _is_outside_matrix(neighbor, char_matrix):
                            next_char = lines[neighbor[0]][neighbor[1]]
                            if next_char == '.':
                                G.add_edge(ij, neighbor)
                    continue

                neighbors = _get_next_neighbors(current_char, ij, char_matrix)
                if not neighbors:
                    continue

                for neighbor in neighbors:
                    G.add_edge(ij, neighbor)

    # Part 1
    paths = list(nx.shortest_path(G, animal_coordinates).values())
    print(f"total_part_1:{len(paths[-1]) -1}")
    
    # Part 2
    animal_component = nx.node_connected_component(G, animal_coordinates)
    components = [G.subgraph(c).copy() for c in nx.connected_components(G) 
                    if not animal_coordinates in c]
    total_part_2 = 0
    nb_line = np.shape(char_matrix)[0]
    for component in components:
        if _is_inside_animal_component(animal_component, component, char_matrix):
            total_part_2 += len(component.nodes)
    print(f"total_part_2:{total_part_2}")


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


def _is_inside_animal_component(animal_component,
                                component,
                                char_matrix):
    '''
    Validate if a component is inside or outside the matrix by counting the horizontal
    lines that must crossed when going vertically from one element of the component to  
    the outside of the animal component. A point is considered inside a polygon if the
    generated line crosses an odd number of sides.
    '''
    nb_line = np.shape(char_matrix)[0]
    # 1 - Do the validation only for one element of the component
    first_ij = next(iter(component))
    if first_ij[0] == 0 or first_ij[0] == nb_line - 1:
        return False

    # 2 - Get horizontal characters below the current element
    nb_horizontal_edge = 0
    horizontal_chars = []
    for i in range(first_ij[0] + 1, nb_line):
        ij = (i, first_ij[1])
        if not ij in animal_component:
            continue
        
        current_char = char_matrix[ij]
        match current_char:
            case '7' | 'J' | 'F' | 'L' | '-':
                horizontal_chars.append(current_char)
            case 'S':
                # TODO : Not hard-code that
                horizontal_chars.append('J')

    # 3 - Count only '-' or horizontal lines that must absolutely be crossed.
    #     In the first example, the dot could be considered slighly on the left of the 
    #     vertical line and the horizontal lines could then be ignored or slightly on the
    #     right and there would be two horizontal lines, that would be ignored below.               
    #     In the second example, one horizontal line must absolutely be crossed in any case.
    #     If the dot is slighly on the left of the vertical line, the horizontal line of the 'J' 
    #     must be crossed. If it's slightly on the right, the horizontal line of the 'F' will  
    #     be crossed.
    #                             .                .
    #                             F                F
    #                             |                |   
    #                             L                J
    while len(horizontal_chars):
        if (horizontal_chars[-1] == '-'):
            horizontal_chars.pop()
            nb_horizontal_edge += 1
        else:
            last_element = horizontal_chars.pop()
            second_to_last_element = horizontal_chars.pop()
            # 0: Left, 1: Right
            horizontal_line_side_dict = {'7' : 0, 'J' : 0, 'F' : 1, 'L' : 1}
            if (horizontal_line_side_dict[last_element] + horizontal_line_side_dict[second_to_last_element]) % 2:
                nb_horizontal_edge +=1 

    return nb_horizontal_edge % 2 


if __name__ == "__main__":
    main()