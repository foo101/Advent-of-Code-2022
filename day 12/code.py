import os

os.chdir("day 12")

# load file into list
data_list = []
for str_in in open("data.txt", "rt"):
    result = str_in[:-1]
    data_list.append(result)

# find the shortest path from starting point S to end point E. You can only move up or down by 1 elevation (m->n or g->f)
# S has elevation a
# E has elevation z
# Since we only care about the shortest path from S to E, we can apply A* pathing algorithm
# (since I don't understand how A* uses node priority to prefer one way to another, Dijkstra algorighm will be used instead)
# Each location is a Node that may or may not be traveled to

locations: list[list['Location']] = []
class Location:
    start: 'Location' = None
    end: 'Location' = None
    def __init__(self, height: str, x: int, y: int):
        self.x: int = x
        self.y: int = y
        match height:
            case 'S':
                self.height: int = ord('a')
                Location.start = self
            case 'E':
                self.height: int = ord('z')
                Location.end = self
            case _:
                self.height: int = ord(height)
        self.neighbours: dict[str, 'Location'] = {}
        self.visited: bool = False
        self.parent: 'Location' = None

    def __repr__(self):
        if self.visited:
            return '░'
        if self == Location.start:
            return 'S'
        if self == Location.end:
            return 'E'
        return chr(self.height)
    
    # the neighbour's height can be at most 1 higher, but any amount lower than self
    def set_neighbours(self, locations: list[list['Location']]) -> None:
        if self.x > 0:
            west = locations[self.y][self.x - 1]
            if west.height - self.height >= -1:
                # print('neighbour: west')
                self.neighbours['west'] = west
        if self.y > 0:
            north = locations[self.y - 1][self.x]
            if north.height - self.height >= -1:
                # print('neighbour: north')
                self.neighbours['north'] = north
        if self.x < len(locations[0]) - 1:
            east = locations[self.y][self.x + 1]
            if east.height - self.height >= -1:
                # print('neighbour: east')
                self.neighbours['east'] = east
        if self.y < len(locations) - 1:
            south = locations[self.y + 1][self.x]
            if south.height - self.height >= -1:
                # print('neighbour: south')
                self.neighbours['south'] = south

    def visit_neighbors(self) -> list['Location']:
        visited_neighbours: list['Location'] = []
        for neighbour in self.neighbours.values():
            self.visited = True
            if neighbour.visited:
                pass
            else:
                neighbour.visited = True
                neighbour.parent = self
                visited_neighbours.append(neighbour)
        return visited_neighbours

    def get_location(self):
        return self.x, self.y

def visit(locations: list[Location]):
    visited_locations = []
    for loc in locations:
        visited = loc.visit_neighbors()
        visited_locations.extend(visited)
    return visited_locations

def show_heightmap(heightmap: list[list[Location]]):
    for row in heightmap:
        for loc in row:
            print(loc, end='')
        print()
    
def get_path(loc: Location) -> int:
    if loc.parent is None:
        # print(loc.get_location())
        return 0
    else:
        # print(loc.get_location())
        return get_path(loc.parent) + 1

# create a heightmap from datalist
heightmap = [[Location(height, x, y) for x, height in enumerate(row)] for y, row in enumerate(data_list)]
# update neighbours for each location
for row in heightmap:
        for loc in row:
            loc.set_neighbours(heightmap)
        print()

print('start:', Location.start.get_location(), 'end:', Location.end.get_location())

# part 1: find distance from start to end
def part_1():
    visited = [Location.end]
    d = 0
    last_visited = []

    while Location.start not in visited:
        if last_visited == visited:
            print('no more neighbors found!')
            show_heightmap(heightmap)
            break
        print('distance from end:', d)
        last_visited = visited
        visited = visit(visited)
        d += 1
    print(Location.start.get_location(), end = ' ')
    print('distance to end:', get_path(Location.start))

#part 2: find the closest location with height 'a' from end
def part_2():
    visited = [Location.end]
    d = 0
    last_visited = []

    while ord('a') not in [loc.height for loc in visited]:
        if last_visited == visited:
            print('no more neighbors found!')
            show_heightmap(heightmap)
            break
        print('distance from end:', d)
        last_visited = visited
        visited = visit(visited)
        d += 1
    found_loc = list(filter(lambda x: x.height == ord('a'), visited))

    for loc in found_loc:
        print(loc.get_location(), end = ' ')
        print('distance to end:', get_path(loc))

part_2()