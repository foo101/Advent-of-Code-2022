import os

from typing import Union
from itertools import zip_longest
import functools

os.chdir("day 13")

# load file into list
data_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    data_list.append(result)

def compare_lists(left: Union[list[any], int], right: Union[list[any], int]):
    '''returns True if left is before right when ordered, else returns False'''
    zipped_list = [*zip_longest(left, right)]
    # print(zipped_list)

    for sub_left, sub_right in zipped_list:
        # print(type(sub_left), type(sub_right))
        if sub_left is None:
            return -1
        if sub_right is None:
            return 1
        if type(sub_left) == list and type(sub_right) == list:
            return compare_lists(sub_left, sub_right)
        if type(sub_left) == list and type(sub_right) == int:
            return compare_lists(sub_left, [sub_right])
        if type(sub_left) == int and type(sub_right) == list:
            return compare_lists([sub_left], sub_right)
        if type(sub_left) == int and type(sub_right) == list:
            return compare_lists([sub_left], sub_right)
        if type(sub_left) == int and type(sub_right) == list:
            return compare_lists([sub_left], sub_right)
        if type(sub_left) == int and type(sub_right) == int:
            if sub_left < sub_right:
                return -1
            elif sub_left > sub_right:
                return 1
            else:
                pass
    return 0

# part 1: summarise all indices of correctly sorted pairs
def part_1():
    sum_of_indices = 0
    for pair_index, i in enumerate(range(0, len(data_list), 3), start=1): # __stop = len(data_list)
        left_str, right_str = data_list[i:i+2]
        if compare_lists(eval(left_str), eval(right_str)) < 1:
            # if correctly sorted
            sum_of_indices += pair_index
    print('sum: ', sum_of_indices)

# part 2: disregard spaces, sort list and find divider packet location
def part_2():
    packet_a = [[2]]
    packet_b = [[6]]
    filtered_list = list(map(eval, filter(lambda t: t != '', data_list)))
    filtered_list.append(packet_a) # add packet_a
    filtered_list.append(packet_b) # add packet_b
    sorted_list = sorted(filtered_list, key=functools.cmp_to_key(compare_lists)) # sort based on compare_lists
    index_a = sorted_list.index(packet_a) + 1 # index starts at 1
    index_b = sorted_list.index(packet_b) + 1 # index starts at 1
    print(index_a * index_b)

part_2()

#part 2: lorem ipsum
