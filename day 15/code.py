import os
import math
import re

os.chdir("day 15")

# data has a list of sensors and their closest beacon. Distance to their closest beacon is calculated with the manhattan distance.
# With this, two assumptions can be made:
# 1) If the distance from position (x, y) to a sensor's (x, y) is smaller or equal than the distance from a sensor's (x, y) to a beacon's (x, y)
# the position cannot be a beacon
# 2) If a sensor's distance (dy) to an (x) row is larger than the sensor's distance to a beacon, its range does not cover any of the positions 
# 
# Since it's faster to calculate which sensors cover what area than it is to calculate which positions are (or are not) covered, 
# combining all the covered areas is faster

# load file into list
data_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    data_list.append(result)

# part 1: for location x=2,000,000, how many locations do NOT contain a beacon
class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other: 'Location'):
        '''override to test on (x, y) in stead of id'''
        if self.__class__ == other.__class__:
            return (self.x, self.y) == (other.x, other.y)
        
    def __hash__(self):
        '''override to test on hash(x, y) because __eq__ is overridden'''
        return hash((self.x, self.y))
    
    def __repr__(self):
        return str(f'({self.x},{self.y})')

    @property
    def frequency(self) -> int:
        '''gives the frequency of a location'''
        return self.x * 4000000 + self.y

    def manhattan_distance(self, other: 'Location'):
        '''returns the manhattan distance to another location (dx + dy)'''
        dx = int(math.fabs(self.x - other.x))
        dy = int(math.fabs(self.y - other.y))
        return dx + dy

class Sensor:
    def __init__(self, sensor_location: Location, beacon_location: Location):
        self.location = sensor_location
        self.beacon = beacon_location
        self.distance_to_beacon = sensor_location.manhattan_distance(beacon_location)

    def __repr__(self):
        return str(self.location)
    
    def get_x_range(self, y: int = 0):
        '''returns a range of x values for a given y where (x, y) is within the sensor's range'''
        dy = int(math.fabs(y - self.location.y))
        d = self.distance_to_beacon - dy
        # x range is from (x - d, y) to (x + d, y)
        return (self.location.x - d, self.location.x + d) if d > 0 else ()

    def get_y_range(self, x: int = 0):
        '''returns a range of y values for a given x where (x, y) is within the sensor's range'''
        dx = int(math.fabs(x - self.location.x))
        d = self.distance_to_beacon - dx
        # x range is from (x - d, y) to (x + d, y)
        return (self.location.y - d, self.location.y + d) if d > 0 else ()
    
def str_to_sensor(str_sensor: str):
    '''takes a string with sensor data and returns a Sensor and Beacon instance'''
    ex = re.compile('(?<==)[-0-9]+')
    f_loc = [*map(int, ex.findall(str_sensor))]
    s_loc = Location(f_loc[0], f_loc[1])
    b_loc = Location(f_loc[2], f_loc[3])
    return Sensor(s_loc, b_loc), b_loc

# save all known sensors and their beacons
sensors: list[Sensor] = []
beacons: list[Location] = []

for str_sensor in data_list:
    s, b = str_to_sensor(str_sensor)
    sensors.append(s)
    beacons.append(b)

# only unique beacons are needed - set uses a == b and hash(a) == hash(b) to compare values (requires __eq__ and __hash__ override)
beacons = list(set(beacons))

def is_overlap(a: tuple[int, int], b: tuple[int, int], give_non_overlapping: bool = False) -> tuple[bool, bool, tuple[int, int], tuple[int, int]]:
    '''compares tuple a with b and returns if it overlaps or contains, along with the ranges of overlap
    requires a[0] <= a[1] and b[0] <= b[1]
    returns:
        overlaps: bool
        contains: bool
    if overlaps = False:
        m as first: tuple[int, int]
        n as second: tuple[int, int]
    if overlaps = True and give_non_overlapping = False:
        m as container range: tuple[int, int]
        n as contained range: tuple[int, int]
    if overlaps = True and give_non_overlapping = True:
        m as range before overlap: tuple[int, int]
        n as range after overlap: tuple[int, int]
    '''
    # if a starts before b
    if a[0] <= b[0]:
        # if b[0] within a:
        if b[0] <= a[1]:
            # if b[1] within a
            if b[1] <= a[1]:
                # b within a
                if give_non_overlapping:
                    # print(f'a{a} b{b} left:{(a[0], b[0] - 1)}, right:{(b[1] + 1, a[1])}')
                    return True, True, (a[0], b[0] - 1), (b[1] + 1, a[1])
                return True, True, a, b
            # b overlaps a
            if give_non_overlapping:
                # print(f'a{a} b{b} left:{(a[0], b[0] - 1)}, right:{(a[1] + 1, b[1])}')
                return True, False, (a[0], b[0] - 1), (a[1] + 1, b[1])
            return True, False, (a[0], b[1]), (b[0], a[1])
        # b after a
        return False, False, a, b
    # a[0] > b[0]
    # TODO: bug a[0] > b[0] and a[1] > b[1] => returns (a[0],b[1]) should be (b[1] + 1, a[1])
    # if a[0] within b:
    if a[0] <= b[1]:
        # if a[1] within b
        if a[1] <= b[1]:
            # a within b
            if give_non_overlapping:
                # print(f'a{a} b{b} left:{(b[0], a[0] - 1)}, right:{(a[1] + 1 , b[1])}')
                return True, True, (b[0], a[0] - 1), (a[1] + 1 , b[1])
            return True, True, b, a
        # a overlaps b
        if give_non_overlapping:
            # print(f'a{a} b{b} left:{(b[0], a[0] - 1)}, right:{(b[1] + 1, a[1])}')
            return True, False, (b[0], a[0] - 1), (b[1] + 1, a[1])
        return True, False, (b[0], a[1]), (a[0], b[1])
    # a after b
    return False, False, b, a

def trim_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    lr_s = sorted(ranges)# key=lambda x: x[0])

    if len(lr_s) == 0 or len(lr_s) == 1:
        return lr_s

    # get all ranges regardless of overlap
    lr_trim = []
    cur = lr_s[0]

    for r in lr_s[1:]:
        overlap, wrap, t_out, t_in = is_overlap(cur, r)
        if(wrap):
            pass
            # print(f'skipped {r}, cur is {cur}')
        elif(overlap):
            cur = t_out
            # print(f'updated {r}, cur is {cur}')
        else:
            # print('added:', cur)
            lr_trim.append(cur)
            cur = r
    # print('added:', cur)
    lr_trim.append(cur)
    return lr_trim

def trim_unknown_ranges(scope: tuple[int, int], ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    known_range = trim_ranges(ranges)
    unknown_range = []

    cur = scope
    for r in known_range:
        overlap, wrap, t_out, t_in = is_overlap(cur, r)
        overlap, wrap, t_left, t_right = is_overlap(cur, r, True)
        if wrap:
            if cur[0] == t_out[0]:
                # range is fully in cur
                unknown_range.append(t_left)
                cur = t_right
            else:
                # cur is fully known
                break
        elif overlap:
            if cur[0] == t_left[0]:
                # cur is left side of overlap
                unknown_range.append(t_left)
            else:
                # cur is right side of overlap
                cur = t_right
        elif cur[0] == t_right[0]:
            # range is before scope, skip range
            pass
        else: # range is after scope, stop trimming
            unknown_range.append(cur)
            break
    return unknown_range

def part_1():
    y=2000000
    sensor_ranges = [*filter(lambda l: len(l) > 0, [s.get_x_range(y) for s in sensors])]
    for s in sensors:
        print(f'sensor {s.location} is {s.distance_to_beacon} away from {s.beacon}')
    
    known_range = trim_ranges(sensor_ranges)
    print(f'known location ranges are {known_range}')

    known_loc = 0
    for r in known_range:
        # location count is from r[0] to r[1], inclusive
        known_loc += r[1] - r[0] + 1
    print (f'known location count is {known_loc}')

    empty_loc = known_loc
    for b in beacons:
        if b.y == y:
            empty_loc -= 1
    print (f'empty location count is {empty_loc}')

    # print(sensor_ranges, total_range)

# part_1()

# part 2: a distress beacon is not within a sensor's range. its location is somewhere between (0,0) and (4000000, 4000000) (inclusive)
# The tuning frequency of any one location can be calculated with:
# f = x * 4000000 + y

def part_2():
    x_min, y_min = 0, 0
    x_max, y_max = 4000000, 4000000

    unknown_locations: list[Location] = []

    for y in range(3186981, 3186982): # range(y_min, y_max + 1)
        if y % 100000 == 0:
            print(f'testing {y}... goal: {y_max}')
        sensor_ranges = [*filter(lambda l: len(l) > 0, [s.get_x_range(y) for s in sensors])]
        unknown_range = trim_unknown_ranges((x_min, x_max), sensor_ranges)
        
        for r in unknown_range:
            print(f'unknown locations found: x={r} at y={y}')
            for x in range(r[0], r[1] + 1):
                # print(f'unknown location found {(x, y)}')
                unknown_locations.append(Location(x, y))

        

    for loc in unknown_locations:
        print(f'Location {loc} has tuning frequency {loc.frequency}')

part_1()
part_2()