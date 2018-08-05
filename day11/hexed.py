import argparse
import logging
import pprint

pp = pprint.PrettyPrinter()

def logsetup(name = 'root'):
    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('event.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

log = logsetup()

parser = argparse.ArgumentParser(description="See instructions.txt")
parser.add_argument("filename", help="The file to read")
args = parser.parse_args()
filename = args.filename
log.info("The file to read is: {}".format(args.filename))

# See: https://www.redblobgames.com/grids/hexagons/
class CubeCoordinate:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.directions = {
            "n": self.n,
            "s": self.s,
            "nw": self.nw,
            "se": self.se,
            "ne": self.ne,
            "sw": self.sw
        }

    def __str__(self):
        return "{}:{}:{}, distance: {}".format(self.x, self.y, self.z, self.distance())
    
    def __repr__(self):
        return self.__str__()

    def n(self):
        self.y += 1
        self.z -= 1

    def s(self):
        self.y -= 1
        self.z += 1

    def nw(self):
        self.y += 1
        self.x -= 1

    def se(self):
        self.y -= 1
        self.x += 1

    def ne(self):
        self.x += 1
        self.z -= 1

    def sw(self):
        self.x -= 1
        self.z += 1

    def move(self, direction):
        func = self.directions[direction]
        func()

    # From looking at the models on the link I have deduced that the distance
    # from the center (starting point) is the sum of all positive coordinates
    # of a position. I.e. that is the minimum number of steps to get back to 
    # the starting point
    def distance(self):
        distance = 0
        if self.x > 0:
            distance += self.x
        if self.y > 0:
            distance += self.y
        if self.z > 0:
            distance += self.z
        return distance        

with open(filename) as file:
    linecounter = 0
    for line in file:
        position = CubeCoordinate()
        if 'test' in filename:
            log.info("Processing TEST data...")
            # The test file is split up to have test data followed by '#' and then a description of the test data
            print("Line {}: {}".format(linecounter, line.strip().split("#")[1].strip()))
            moves = line.split("#")[0].strip().split(',')
        else:
            log.info("Processing PRODUCTION data...")
            moves = line.strip().split(',')
        for direction in moves:
            position.move(direction)
        print("Coordinates: {}".format(position))
        linecounter += 1
