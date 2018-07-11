# Approach #2 - just travel the way and keep track off coordinates as we go
# origo is where 1 is located

import math

def is_even(number):
    return (number %2 == 0)

def calc_segmentstart(base):
    endpoint = base * base
    return endpoint - base - base + 2


def travel(goal):
    coord = [0,0]
    distance = 0
    current_corner = 1
    current_base = 1
    if (is_even(base)):
        direction = 'left'
    else:
        direction = 'right'
    # 
    next_corner = find_next_corner(base+1)

####################
# add base until we are passed the target then backtrack to the target

# Given a certain index - how big must the spiral grid side be to hold that index?
# It comes down to finding out the first squared number that is larger than 
# or equal to the index.
def calulate_grid_base(index):
    root = int(math.floor(math.sqrt(index)))
    if (root*root == index):
        return root
    return root+1

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

def spiral_to(target):
    base = calulate_grid_base(target)
    coord = [0,0,1]
    index = 1
    direction = 'right'

    current_segment = 1
    current_segment_end = 1

    while (current_segment < base):
        nextsegment = current_segment+1
        nextsegment_size = calc_segmentsize(nextsegment)
        nextsegment_end = current_segment_end + nextsegment_size
        corner1 = current_segment_end + 1
        corner2 = corner1 + ((nextsegment_size - 1) / 2)
        # print("Corners for #{} are {} and {}. Segment has size {} and ends at {}".format(nextsegment, corner1, corner2, nextsegment_size, nextsegment_end))

        while ((index < target) and (index <= nextsegment_end)):
            if ((index == corner1) or (index == corner2)):
                direction = get_direction(direction)
            # print("Coordinates and index: {}, facing {}".format(coord, direction))  
            if (direction == 'right'):
                coord[0] += 1
            if (direction == 'left'):
                coord[0] -= 1
            if (direction == 'up'):
                coord[1] += 1
            if (direction == 'down'):
                coord[1] -= 1
            index += 1
            coord[2] = index

        current_segment += 1
        current_segment_end = index - 1

    return coord

def calc_distance(target):
    result = spiral_to(target)
    print("Spiraling to {} gives us: {}".format(target, result))

    xsteps = abs(result[0])
    ysteps = abs(result[1])
    steps = xsteps + ysteps
    print("Steps to origo are {}".format(steps))

calc_distance(1)
calc_distance(12)
calc_distance(23)
calc_distance(1024)
calc_distance(312051)
