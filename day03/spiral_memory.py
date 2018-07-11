# Note: Abandonded this path of solving the problem for now...

import math

def assertEquals(actual, expected):
    success = actual == expected
    print("Actual: {}, expected {}, Correct? {}".format(actual, expected, success))
    return success

# Given a certain index - how big must the spiral grid side be to hold that index?
# It comes down to finding out the first squared number that is larger than 
# or equal to the index.
def calulate_grid_base(index):
    root = int(math.floor(math.sqrt(index)))
    if (root*root == index):
        return root
    return root+1

def test_calulate_grid_base():
    assertEquals(1,calulate_grid_base(1))
    assertEquals(2,calulate_grid_base(2))
    assertEquals(2,calulate_grid_base(3))
    assertEquals(2,calulate_grid_base(4))
    assertEquals(3,calulate_grid_base(5))
    assertEquals(3,calulate_grid_base(6))
    assertEquals(3,calulate_grid_base(7))
    assertEquals(3,calulate_grid_base(8))
    assertEquals(3,calulate_grid_base(9))
    assertEquals(5,calulate_grid_base(17))
    assertEquals(5,calulate_grid_base(25))
    assertEquals(6,calulate_grid_base(26))
    assertEquals(559,calulate_grid_base(312051))


#test_calulate_grid_side()
input = 312051
grid_side = calulate_grid_base(input)
print("Grid side for input {} is {}".format(input, grid_side))

# Based on the grid side length we can figure out the id of the last cell
# and the total length of the last 'lap' of the spiral and use those numbers
# to determine where to find the cell we are looking for.
# odd squares go off in lower right corner, even squares in the top left corner.

def is_even_grid(number):
    if ((number*number)%2 == 0):
        return True
    return False

# Calc the length of the last lap of the spiral
# base * 4 would count each corner two times so we subtract 4
def calc_circumference(base):
    return (base * 4) - 4

# A segment is the range that was added by the last 'layer'
# For base = 2 the section added would be the range [2,3,4] 
# as the previous section was just [1] and 2*2 = 4 so the section contains 
# all numbers after the previous section up to and including the result of 2*2.
# For base = 7 the section up to 7*7 would be 6*6+1 to 7*7, i.e. 37 to 49.
# For base = 4 the section up to 4*4 would be 3*3+1 to 4*4, i.e. 10 to 16
# Each section adds base + (base - 1) cells.
# So endpoint - base - base + 2 gives us the index of the first cell in the section
def calc_segmentstart(base):
    endpoint = base * base
    return endpoint - base - base + 2

def get_lap_start(base):
    circumference = calc_circumference(base)
    start = base*base-circumference+1
    return start   

def do_calculate(testinput):
    base = calulate_grid_base(testinput)
    endpoint = base*base
    circumference = calc_circumference(base)
    segmentstart = calc_segmentstart(base)
    print("For input {} we get base {}, circumference {}, segmentstart {}".format(testinput, base, circumference, segmentstart))

    print(range(segmentstart, endpoint+1))

    # If segmentstart-1 is odd we start in upper left corner 



do_calculate(42)
