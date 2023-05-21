import os

def split_pair(pair_str):
    pair_split = pair_str.split(',')
    for i in range(len(pair_split)):
        pair_split[i] = list(map(int, pair_split[i].split('-')))
    return pair_split

def is_fully_contained(pair):
    # print(' ' * (pair[0][0] - 1) + '-' * (pair[0][1] - pair[0][0]), sep = '')
    # print(str(' ' * (pair[1][0] - 1) + '-' * (pair[1][1] - pair[1][0])).ljust(100), sep = '', end='')
    if (pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]) or (pair[1][0] <= pair[0][0] and pair[1][1] >= pair[0][1]):
        # print("yes")
        return True
    # print("no")
    return False

def is_overlapping(pair):
    # print(' ' * (pair[0][0] - 1) + '-' * (pair[0][1] - pair[0][0]), sep = '')
    # print(str(' ' * (pair[1][0] - 1) + '-' * (pair[1][1] - pair[1][0])).ljust(100), sep = '', end='')
    
    if not ((pair[0][0] < pair[1][0] and pair[0][1] < pair[1][0]) or (pair[0][0] > pair[1][1] and pair[0][1] > pair[1][1])): # find non-overlapping, return opposite
        # print("yes")
        return True
    # print("no")
    return False

os.chdir("day 4")

# load file into list
pair_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    pair_list.append(result)


# part 1: find all pairs in which one range is fully contained in another
pair_split_list = list(map(split_pair, pair_list))
filtered_list = list(filter(is_fully_contained, pair_split_list))
print("fully contained pairs:", len(filtered_list))

#part 2: lorem ipsum

filtered_list = list(filter(is_overlapping, pair_split_list))
print("overlapping pairs:", len(filtered_list))