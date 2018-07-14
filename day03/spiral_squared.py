# Day 3, part 2

# Coordinate system:
# Dictionary with key='[x,y]' and value='value'
# If no value at given key then default to 0

# We can still spiral away the same way but we need to calculate adjacent coordinates and 
# look for any existing neighbours before determining what value to put in a cell.

class Cell:
    def __init__(self, x, y, index, value):
        self.x = x
        self.y = y
        self.index = index
        self.value = value

    def __str__(self):
        return "{}:{}:{}:{}".format(self.x, self.y, self.index, self.value)

def get_key(x, y):
    return "{}:{}".format(x,y)

def get_direction(direction):
    if (direction == 'right'):
        return 'up'
    if (direction == 'left'):
        return 'down'
    if (direction == 'up'):
        return 'left'
    if (direction == 'down'):
        return 'right'

def calc_segmentsize(base):
    return base + base -1

def get_neighbours(x, y):
    return [
        # Column to the left:
        get_key(x-1,y+1),
        get_key(x-1,y),
        get_key(x-1,y-1),
        # Column to the center, excluding center:
        get_key(x,y+1),
        get_key(x,y-1),
        # Column to the right:
        get_key(x+1,y+1),
        get_key(x+1,y),
        get_key(x+1,y-1)
    ]

def calculate_from_neighbours(x, y, grid):
    neighbours = get_neighbours(x, y)
    total = 0
    for key in neighbours:
        if key in grid:
            total += grid[key].value
    if (total == 0):
        # First cell should have value: 1
        total = 1
    return total

def spiral_passed(target_value):
    grid = {
        get_key(0,0): Cell(0,0,1,1)
    }
    cursor = [0,0,1]
    index = 1
    direction = 'right'

    current_segment = 1
    current_segment_end = 1

    calculating = True

    while (calculating):
        nextsegment = current_segment+1
        nextsegment_size = calc_segmentsize(nextsegment)
        nextsegment_end = current_segment_end + nextsegment_size
        corner1 = current_segment_end + 1
        corner2 = corner1 + ((nextsegment_size - 1) / 2)
        # print("Corners for #{} are {} and {}. Segment has size {} and ends at {}".format(nextsegment, corner1, corner2, nextsegment_size, nextsegment_end))

        while (calculating and (index <= nextsegment_end)):
            if ((index == corner1) or (index == corner2)):
                direction = get_direction(direction)
            # print("Coordinates and index: {}, facing {}".format(cursor, direction))  
            if (direction == 'right'):
                cursor[0] += 1
            if (direction == 'left'):
                cursor[0] -= 1
            if (direction == 'up'):
                cursor[1] += 1
            if (direction == 'down'):
                cursor[1] -= 1
            index += 1
            cursor[2] = index
            x = cursor[0]
            y = cursor[1]
            key = get_key(x, y)
            value = calculate_from_neighbours(x, y, grid)
            new_cell = Cell(x,y,index,value)
            print(new_cell)
            grid[key] = Cell(x,y,index,value)
            if (value >= target_value):
                return new_cell

        current_segment += 1
        current_segment_end = index - 1

def calc_sums(target):
    res = spiral_passed(target)
    print("Input {} gives result {}".format(target, res))

#calc_sums(1)
#calc_sums(2)
#calc_sums(3)
#calc_sums(4)
#calc_sums(5)
#calc_sums(12)
#calc_sums(23)
#calc_sums(1024)
calc_sums(312051)
