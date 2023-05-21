import os

def get_item_priority(item):
    if str.islower(item):
        return (ord(item) - ord('a') + 1)
    elif str.isupper(item):
        return (ord(item) - ord('A') + 27)
    else:
        raise ValueError()
    
def compare_pockets(pocket_a, pocket_b):
    duplicate_items = ""
    for item_a in sorted(pocket_a):
        for item_b in sorted(pocket_b):
            if item_a < item_b:
                break
            elif item_a == item_b:
                duplicate_items += item_a
    return "".join(set(duplicate_items))


os.chdir("day 3")

# load file into list
rucksacks_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    rucksacks_list.append(result)
    # print(pockets_list)

# part 1: search for duplicate items in left and right pocket, and convert to a priority
sum_of_item_priorities = 0
for rucksack in rucksacks_list: # check each rucksack
    rucksack_item_amount = len(result)
    pockets_list = [result[:rucksack_item_amount // 2], result[-rucksack_item_amount // 2:]]

    duplicate_items = compare_pockets(pockets_list[0], pockets_list[1])
    for item in duplicate_items:
        sum_of_item_priorities += get_item_priority(item)

print(sum_of_item_priorities)

#part 2: search for common items between 3 elves, and convert to a priority (group number)
sum_of_group_priorities = 0
for i in range(len(rucksacks_list) // 3):
    duplicate_items = compare_pockets(compare_pockets(rucksacks_list[i * 3], rucksacks_list[i * 3 + 1]), rucksacks_list[i * 3 + 2]) # compare rucksack 1 and 2, then compare duplicate items with rucksack 3
    print(duplicate_items)
    for item in duplicate_items:
        sum_of_group_priorities += get_item_priority(item)

print(sum_of_group_priorities)