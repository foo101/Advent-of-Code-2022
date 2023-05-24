import os

os.chdir("day 9")

# header H follows a certain path determined by attached file Data.txt, tail T follows header H by trailing behind H, with a maximum distance of 1
# goal: count all locations tail T visited at least once
# data contains the motions of header H with the following format
# movement (letter): L|U|R|D (left, up, right, down), then value(int) (amount to move in that direction)

# header H and tail T always start at location (0,0)

# tail T trails behind H with the following logic:
# if H is more than 1 away, tail T trails behind
# horizontal:
# ...    ...    ...
# TH. -> T.H -> .TH
# ...    ...    ...
# vertical
# .T.    .T.    ...
# .H. -> ... -> .T.
# ...    .H.    .H.
# diagonal: (note that diagonal movement of T takes priority)
# .T.    .T.    ...
# ..H -> ... -> ..T
# ...    ..H    ..H

chain_len = 10 # 2 for part 1, 10 for part 2

def add(tup_a: tuple[any], tup_b: tuple[any]) -> tuple[any]:
    return tuple([tup_a[i] + tup_b[i] for i in range(len(tup_a))])

def sub(tup_a: tuple[any], tup_b: tuple[any]) -> tuple[any]:
    return tuple([tup_a[i] - tup_b[i] for i in range(len(tup_a))])

def get_tail_position(header: tuple[int, int], tail: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    '''finds new position of tail based on distance from header'''
    
    dx, dy = sub(header, tail)

    # check if header is more than 2 knots away from tail
    is_tail_moving = False
    if dx < -1:
        is_tail_moving = True
        dx = -1
    if dx > 1:
        is_tail_moving = True
        dx = 1
    if dy < -1:
        is_tail_moving = True
        dy = -1
    if dy > 1:
        is_tail_moving = True
        dy = 1

    # if tail is moving, calculate new tail position. note that this prioritises diagonal movement
    if is_tail_moving:
        tail = add(tail, (dx, dy))

    return tail

def get_new_positions(chain: list[tuple[int, int]], header_movement: tuple[int, int]) -> list[tuple[int, int]]:
    new_chain = []

    # calculate new header location for testing tail movement
    new_header = add(chain[0], header_movement)
    new_chain.append(new_header)
    # get new positions of every next node in the chain based on new node position
    for tail in chain[1:]:
        new_tail = get_tail_position(new_chain[-1], tail)
        new_chain.append(new_tail)
    return new_chain



chain_pos_list = [] # create an empty chain

# populate chain with nodes at start position (0,0)
chain_pos_list.append([(0,0) for i in range(chain_len)])

def log_movement(direction: str, amount: int) -> None:
    direction_to_movement = {'U': (0, 1), 'R': (1, 0), 'D': (0, -1), 'L':(-1, 0)}
    delta_H_pos = direction_to_movement[direction]

    # log new positions of header and tail
    for i in range(amount):
        new_chain_pos = get_new_positions(chain_pos_list[-1], delta_H_pos)
        chain_pos_list.append(new_chain_pos)
        

# load file into list
H_dir_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]

    #split input, convert 2nd part to int

    movement_str = result.split(' ')
    movement = (movement_str[0], int(movement_str[1]))
    H_dir_list.append(movement)


# log the movement of header and tail for every step 
for direction, amount in H_dir_list:
    log_movement(direction, amount)

ordered_chain_list = list(zip(*chain_pos_list))
# part 1, 2: get all unique tail positions

print('chain length:', len(ordered_chain_list))
print('Total locations traveled:', len(chain_pos_list))

for i, node_pos_list in enumerate(ordered_chain_list):
    print('node', i, 'traveled ', len(list(set(node_pos_list))), 'locations')

