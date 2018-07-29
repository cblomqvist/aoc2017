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

class CircularList:
    def __init__(self, size):
        self.list = []
        for i in range(0,size):
            self.list.append(i)
        self.size = size
        self.pos = 0
        self.skipsize = 0
    
    def __str__(self):
        return "pos: {}, skip: {}, list: {}".format(self.pos, self.skipsize, self.list)
    
    def __repr__(self):
        return self.__str__(self)

    def twist(self, length):
        log.info("Before twist: {}, length: {}".format(self, length))
        # Create a sub-list starting at self.pos with length = length, 
        # possibly wrapping past position 255.
        remaining = self.size - self.pos
        sub1 = None
        sub2 = None
        if remaining <= length:
            # This sub-list will wrap
            length1 = remaining
            sub1 = self.list[self.pos:self.size]
            length2 = length-remaining
            sub2 = self.list[0:length-remaining]
            sublist = sub1 + sub2
        else:
            sublist = self.list[self.pos:self.pos+length]

        log.info("Sublist: {}".format(sublist))
        # Reverse that sub-list
        sublist.reverse()
        log.info("Reverse: {}".format(sublist))

        # Replace section in self.list with the sub-list
        if sub1 == None:
            # Simple replacement
            self.list[self.pos:self.pos+length] = sublist
        else:
            # Complex replacement with wrapping
            self.list[self.pos:self.size] = sublist[0:length1]
            self.list[0:length2] = sublist[length1:]
    
        # Increase pos by length + self.skipsize
        self.pos += length + self.skipsize
        if self.pos >= self.size:
            self.pos = self.pos % self.size

        # Increase self.skipsize by 1 for the next round
        self.skipsize += 1

    def multiply_two_first(self):
        return int(self.list[0]) * int(self.list[1])

def process_input(size, input):
    circle = CircularList(size)
    for i in input:
        circle.twist(int(i))
    print("Circle: {}".format(circle))
    print("multiply_two_first: {}".format(circle.multiply_two_first()))

with open(filename) as file:
    # newline allows us to test multiple datastreams in a testfile
    # the real input data has only one line
    linecounter = 1
    for line in file:
        input = line.strip().split(",")

        # Char by char then process the data to find groups and scores
        if 'test' in filename:
            # The test file is split up to have test data followed by '#' and then a descrition of the test data
            print("Line {}: {}".format(linecounter, line.strip()))
            process_input(5, input)
            linecounter += 1
        else:
            process_input(256, input)
