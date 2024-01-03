# Standard library import
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 19",
                                     description="Check https://adventofcode.com/2023/day/19 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    workflows_dict = {}
    part_ratings = []
    with open(args.filename, 'r') as f:
        file_content = f.read()
        workflows, part_ratings_str = file_content.split('\n\n')

        # Get input
        for part_rating_str in part_ratings_str.split('\n'):
            rate_per_category = {}
            rates = part_rating_str[1:-1].split(',')
            for rate in rates:
                rate_per_category[rate[0]] = int(rate[2:])
            part_ratings.append(rate_per_category)

        # Get workflows
        for workflow in workflows.split('\n'):
            workflow_name, workflow_content = workflow.split('{')
            workflows_dict[workflow_name] = workflow_content[:-1]
        
        # Represent workflows as binary tree
        root_node = build_tree_from_input(workflows_dict)
        
        # Part 1
        total_part_1 = 0
        for part_rating in part_ratings:
            if part_rating_is_valid(root_node, part_rating):
                total_part_1 += sum(part_rating.values())
        print(total_part_1)


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
    def __str__(self):
        return f"{self.data}"


def build_tree_from_input(workflows_dict):
    def build_tree_helper(workflows_dict, current_condition):
        if current_condition in {'R', 'A'}:
            return TreeNode(current_condition)
        if current_condition in workflows_dict:
            return build_tree_helper(workflows_dict, workflows_dict[current_condition])

        first_workflow, child_right_workflow = current_condition.split(',', 1)
        first_condition, child_left_workflow = first_workflow.split(':')

        node       = TreeNode(first_condition)
        node.left  = build_tree_helper(workflows_dict, child_left_workflow)
        node.right = build_tree_helper(workflows_dict, child_right_workflow)
        return node

    # Build binary tree
    root_node = build_tree_helper(workflows_dict, workflows_dict['in'])
    return root_node

    
def part_rating_is_valid(root, part_rating):
    stack = [root]
    while stack:
        node = stack.pop()
        if node.data == 'A':
            return True

        if node.data == 'R':
            return False

        char = node.data[0]
        op = node.data[1]
        value = int(node.data[2:])

        if eval(f"{part_rating[char]}{op}{value}"):
            stack.append(node.left)
        else:
            stack.append(node.right)
    return False


if __name__ == "__main__":
    main()


