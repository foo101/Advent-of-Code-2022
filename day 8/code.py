import os
from dataclasses import dataclass

os.chdir("day 8")

@dataclass
class Tree:
    height: int
    scenic_score = 1
    is_visible: bool = False

# load file into list
data_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    data_list.append(result)

forest = [] # list[list[Tree]] | None 2d list of trees

def populate_forest(data: list[str]) -> list[list[Tree]]:
    # make a list of characters, for each character create a Tree
    forest = []
    for row in data:
        tree_row = list(map(lambda t: Tree(t), row))
        forest.append(tree_row)
    return forest

forest = populate_forest(data_list)

# go from top left to bottom right
for row in range(len(forest)): 
    for col in range(len(forest[0])):
        # is visible from left, adds scenic score of left side of tree
        for other_tree_in_col in range(col - 1, -1, -1):
            if forest[row][other_tree_in_col].height >= forest[row][col].height:
                # blocked
                forest[row][col].scenic_score *= col - other_tree_in_col
                break
        else:
            forest[row][col].scenic_score *= col
            forest[row][col].is_visible = True

        # is visible from top
        for other_tree_in_row in range(row - 1, -1, -1):
            if forest[other_tree_in_row][col].height >= forest[row][col].height:
                # blocked
                forest[row][col].scenic_score *= row - other_tree_in_row
                break
        else:
            # not blocked
            forest[row][col].scenic_score *= row
            forest[row][col].is_visible = True
                
# go from bottom right to top left
for row in range(len(forest) - 1, -1, -1): 
    for col in range(len(forest[0]) - 1, -1, -1):
        # is visible from right
        for other_tree_in_col in range(col + 1, len(forest[0])):
            if forest[row][other_tree_in_col].height >= forest[row][col].height:
                # blocked
                forest[row][col].scenic_score *= other_tree_in_col - col
                break
        else:
            # not blocked
            forest[row][col].scenic_score *= len(forest[0]) - col - 1
            forest[row][col].is_visible = True

        # is visible from bottom
        for other_tree_in_row in range(row + 1, len(forest)):
            if forest[other_tree_in_row][col].height >= forest[row][col].height:
                # blocked
                forest[row][col].scenic_score *= other_tree_in_row - row
                break
        else:
            # not blocked
            forest[row][col].scenic_score *= len(forest) - row -1
            forest[row][col].is_visible = True

# part 1: give the amount of trees visible from the outside
# part 2: find the tree with highest scenic view
visible_count = 0
max_scenic_view = 0

for row in forest:
    for tree in row:
        if tree.is_visible: 
            visible_count += 1
        if tree.scenic_score > max_scenic_view:
            max_scenic_view = tree.scenic_score
        print('[', str(tree.height).rjust(3, ' '), str(tree.scenic_score).rjust(3, ' '), '] ', sep='', end='')
    print()

print('trees visible:', visible_count)

print("highest scenic score:", max_scenic_view)