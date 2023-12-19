# Standard library import
import argparse
import logging
import os


def main():
    parser = argparse.ArgumentParser(prog="Advent of code 2023 - day 12",
                                     description="Check https://adventofcode.com/2023/day/12 \
                                                  to see the problem solved by this script.")
    parser.add_argument("filename", help="File to parse")
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logging.error(f"File {args.filename} does not exist.")

    lines = []
    total_part_1 = 0
    with open(args.filename, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            records, arrangement = line.split()
            arrangement = [int(group_length) for group_length in arrangement.split(',')]
            total_part_1 += _number_of_arrangements(records, arrangement)
    print(f"total_part_1:{total_part_1}")

    total_part_2 = 0
    for line in lines:
        initial_records, initial_arrangement = line.split()
        initial_arrangement = [int(group_length) for group_length in initial_arrangement.split(',')]
        
        records = 4 * (initial_records + '?') + initial_records
        arrangement = 5 * initial_arrangement
        total_part_2 += _number_of_arrangements(records, arrangement)

    print(f"total_part_2:{total_part_2}")


def _number_of_arrangements(record : str, 
                            arrangement : list[int],
                            arrangement_cache = {}):
    '''
    Function to get the number of possible arrangements for a given record and an
    arrangement.
    '''
    if not record:
        return 0 if arrangement else 1
    
    current_char = record[0]
    if current_char == '.':
        return _number_of_arrangements_recursive_call(record[1:], 
                                                      arrangement, 
                                                      arrangement_cache)
    if current_char == '?':
        return _number_of_arrangements_recursive_call('.' + record[1:], 
                                                      arrangement, 
                                                      arrangement_cache) + \
               _number_of_arrangements_recursive_call('#' + record[1:], 
                                                      arrangement, 
                                                      arrangement_cache)
    if current_char == '#':
        if not arrangement:
            return 0
        i = 0
        while i < len(record) and record[i] == '#':
            i += 1

        if i < len(record) and record[i] == '?':
            hashtags = '#' * i
            return _number_of_arrangements_recursive_call(hashtags + '#' + record[i + 1:], 
                                                          arrangement, 
                                                          arrangement_cache) + \
                   _number_of_arrangements_recursive_call(hashtags + '.' + record[i + 1:], 
                                                          arrangement,
                                                          arrangement_cache)
        else:
            arrangement_copy = arrangement.copy()
            sub_group_size = arrangement_copy.pop(0)
            if i != sub_group_size:
                return 0
            else:
                return _number_of_arrangements_recursive_call(record[i + 1:], 
                                                              arrangement_copy, 
                                                              arrangement_cache)

    logging.error(f"Exited function without returning number.")  


def _number_of_arrangements_recursive_call(record : str, 
                                           arrangement : list[int],
                                           arrangement_cache : dict[tuple[int], int]):
    ''' 
    Function to get the number of arrangements. It is not in the cache, it will compute
    the result add it to the cache.
    '''
    key = (record, tuple(arrangement))
    if key in arrangement_cache:
        return arrangement_cache[key]
    
    number_of_arrangements = _number_of_arrangements(record, 
                                                     arrangement, 
                                                     arrangement_cache)
    arrangement_cache[key] = number_of_arrangements
    
    return number_of_arrangements


if __name__ == "__main__":
    main()