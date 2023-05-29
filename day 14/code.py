import os

os.chdir("day 14")

# advent of code day 14: regolith reservoir
# find the path behind the waterfall
# the import data reports the x,y coordinates that form the shape of the path of a solid rock structure
# x represents the shape to the right
# y represents the shape down
# 
# ex:
# 498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
# 
# there are 2 rock structures: 
# one leads from (498, 4) to (498, 6), and from there to (496, 6)
# one leads from (503, 4) to (502, 4), from there to (502, 9), to (498, 9)
#
#   4444445555
#   9999990000
#   4567890123
# 0 ......+...
# 1 ..........
# 2 ..........
# 3 ..........
# 4 ....#...##
# 5 ....#...#.
# 6 ..###...#.
# 7 ........#.
# 8 ........#.
# 9 #########.

# sand is pouring in from (500, 0), with 1 particle at a time.
# If a particle can fall straight down, it will.
# ...    ...
# .o. -> ...
# ...    .o.
# if not: if it can roll to the left, it will
# ...    ...
# .o. -> ...
# .#.    o#.
# if not: if it can roll to the right, it will
# ...    ...
# .o. -> ...
# ##.    ##o
# if none of the above: it stays put
# ...    ...
# .o. -> .#.
# ###    ###
# 
# find how many particles it takes before one passes the structure (falls into the void)

# load file into list
data_list: list[str] = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    data_list.append(result)

# keep track of sand source coordinates in area
source_repr_x, source_repr_y = 500, 0 # represents sand source coordinates, immutable
area_repr_x, area_repr_y = 500, 0 # represents the coordinates of the top left area coordinate, mutable

area = [['+']] # area is a 2d list of locations represented as list of strings, can be searched through with area[x][y]

def expand_area(x: int, y: int) -> None:
    global area_repr_x, area_repr_y, area # dangerous but it works well enough
    area_x, area_y = len(area[0]), len(area)
    # print('area:', area_x, area_y)

    dx_left, dx_right = area_repr_x - x, -((area_repr_x + area_x) - x)
    dy_up, dy_down = -(y - area_repr_y), y - (area_repr_y + area_y)

    # expand area up and down
    for i in range(dy_up):
        area.insert(0, ['.' for i in range(area_x)])
    for j in range(dy_down + 1):
        area.append(['.' for i in range(area_x)])
    if(dy_up > 0):
        area_repr_y -= dy_up

    # expand area left and right
    for row in area:
        for i in range(dx_left):
            row.insert(0, '.')
        for j in range(dx_right + 1):
            row.extend('.')
    if dx_left > 0:
        area_repr_x -= dx_left
    
    # debugging area expansion
    # print('dx:', dx_left, dx_right)
    # print('dy:', dy_up, dy_down)
    
def block(shape_start_x: int, shape_start_y: int, shape_end_x: int, shape_end_y: int):
    global area_repr_x, area_repr_y, area # dangerous but it works well enough
    area_x, area_y = len(area[0]), len(area)
    move_x, move_y = shape_end_x - shape_start_x, shape_end_y - shape_start_y

    # print(f'area size: {area_x} {area_y}')
    # print(f'start: {shape_start_x - area_repr_x} {shape_start_y - area_repr_y}')
    # print(f'move: {move_x} {move_y}')

    if move_x > 0:
        for dx in range(move_x + 1):
            area[shape_start_y - area_repr_y][shape_start_x - area_repr_x + dx] = '#'
    elif move_x < 0:
        for dx in range(0, move_x - 1, -1):
            area[shape_start_y - area_repr_y][shape_start_x - area_repr_x + dx] = '#'
    if move_y > 0:
        for dy in range(move_y + 1):
            area[shape_start_y - area_repr_y + dy][shape_start_x - area_repr_x] = '#'
    elif move_y < 0:
        for dy in range(0, move_y - 1, -1):
            area[shape_start_y - area_repr_y + dy][shape_start_x - area_repr_x] = '#'

for shape_str in data_list: # create an area and fill with shapes
    shape = list(map(lambda x: list(map(int, x.split(','))), shape_str.split(' -> ')))

    # expand area if necessary
    print(shape)
    for loc_x, loc_y in shape:
        expand_area(loc_x, loc_y)

    shape_start_x = shape_start_y = None
    for loc_x, loc_y in shape:
        if shape_start_x == None:
            shape_start_x, shape_start_y = loc_x, loc_y
        else:
            block(shape_start_x, shape_start_y, loc_x, loc_y)
            shape_start_x, shape_start_y = loc_x, loc_y
expand_area(area_repr_x, area_repr_y + len(area) + 1) # add padding

print('blank area:')
for row in area:
    for loc in row:
        print(loc, end='')
    print()
print()

class SimulationFinished(Exception): ...
def simulate_particle(particle_x: int, particle_y: int, has_floor: bool = False) -> tuple[int, int, bool]:
    global area_repr_x, area_repr_y, area # dangerous but it works well enough
    x, y = particle_x - area_repr_x, particle_y - area_repr_y
    try:
        if y + 1 >= area_repr_y + len(area):
            raise SimulationFinished()
        
        if x - 1 < 1:
            x += 1
            expand_area(area_repr_x - 1, area_repr_y)
            if(has_floor):
                area[len(area) - 1][0] = '#'
        elif x + 1 >= len(area[0]) - 1:
            expand_area(area_repr_x + len(area[0]), area_repr_y)
            if(has_floor):
                area[len(area) - 1][len(area[0]) - 1] = '#'

        test_loc = area[y + 1][x]
        if test_loc == '.' or test_loc == '~':
            area[y + 1][x] = '~'
            return (particle_x, particle_y + 1, False)
        test_loc = area[y + 1][x - 1]
        if test_loc == '.' or test_loc == '~':
            area[y + 1][x - 1] = '~'
            return (particle_x - 1, particle_y + 1, False)
        test_loc = area[y + 1][x + 1]
        if test_loc == '.' or test_loc == '~':
            area[y + 1][x + 1] = '~'
            return (particle_x + 1, particle_y + 1, False)
        # else
        area[y][x] = 'o'
        return (particle_x, particle_y, True)
    except IndexError:
        raise IndexError

# part 1: test the amount of particles before one reaches the floor
def part_1():
    finished = False
    particles = 0
    x, y = source_repr_x, source_repr_y
    particle_at_rest = False
    while not finished:
        x, y = source_repr_x, source_repr_y
        particle_at_rest = False
        while not particle_at_rest:
            try:
                x, y, particle_at_rest = simulate_particle(x, y)
            except SimulationFinished:
                finished = True
                break
        else:
            if y == source_repr_y:
                finished = True
            particles += 1


    print('filled area:')
    for row in area:
        for loc in row:
            print(loc, end='')
        print()
    print()

    print(f'amount of simulated particles before none could be added: {particles}')

# part 2: the floor is 2 units under the shape, thest the amount of particles before one comes to rest at (500,0)
def part_2():
    # area has a floor:
    for i in range(len(area[0])):
        area[len(area) - 1][i] = '#'

    
    finished = False
    particles = 0
    x, y = source_repr_x, source_repr_y
    particle_at_rest = False
    while not finished:
        x, y = source_repr_x, source_repr_y
        particle_at_rest = False
        while not particle_at_rest:
            try:
                # has a floor
                x, y, particle_at_rest = simulate_particle(x, y, True)
                if y == source_repr_y:
                    particles += 1
                    finished = True
                    break
            except SimulationFinished:
                finished = True
                break
        else:
            particles += 1


    print('filled area:')
    for row in area:
        for loc in row:
            print(loc, end='')
        print()
    print()

    print(f'amount of simulated particles before none could be added: {particles}')

part_2()