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
        log.debug("Before twist: {}, length: {}".format(self, length))
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

        log.debug("Sublist: {}".format(sublist))
        # Reverse that sub-list
        sublist.reverse()
        log.debug("Reverse: {}".format(sublist))

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

def part1():
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

########################################3
# Additions for part 2
########################################3

class HashCircle(CircularList):

    def __init__(self, size):
    #     self.list = []
    #     for i in range(0,size):
    #         self.list.append(i)
    #     self.size = size
    #     self.pos = 0
    #     self.skipsize = 0
        super().__init__(size)
        self.dense = ""

    def dense_hash(self):
        log.debug("LIST: {}".format(self.list))
        start = 0
        end = 0
        length = 16
        blocks = []
        while end < 256:
            end = start + length
            blocks.append(self.list[start:end])
            start = end

        log.debug("BLOCKS: {}".format(blocks))
        for block in blocks:
            value = None
            for i in block:
                if value == None:
                    value = i
                    continue
                value = value ^ i
            # Convert the resulting int to string and format it as a hex value
            log.debug("INTVALUE: {}".format(value))
            hexvalue = format(value, 'x')
            if len(hexvalue) == 1:
                hexvalue = '0' + hexvalue
            log.debug("HEXVALUE: {}".format(hexvalue))
            self.dense += hexvalue
        return self.dense

def convert_to_ascii_list(line):
    input = line.strip()
    result = []
    for i in input:
        result.append(ord(i))
    return result

def process_input_in_circle(circle, input):
    for i in input:
        circle.twist(i)

def part2_process_line(line):
    circle = HashCircle(256)
    input = convert_to_ascii_list(line)
    log.debug("LINE: {}".format(line))
    log.debug("INPUT: {}".format(input))
    # Sequence of 5 lengths to always add to the input
    input += [17, 31, 73, 47, 23]
    log.debug("INPUT: {}".format(input))

    # Byte by byte then process the data to find groups and scores
    number_of_rounds = 64
    for round in range(0, number_of_rounds):
        process_input_in_circle(circle, input)
    print("Circle: {}".format(circle))
    print("multiply_two_first: {}".format(circle.multiply_two_first()))
    dense = circle.dense_hash()
    print("Dense Hash: {}".format(dense))

def part2():

    # Test cases:
    # The empty string becomes a2582a3a0e66e6e86e3812dcb672a272.
    # AoC 2017 becomes 33efeb34ea91902bb2f59c9920caa6cd.
    # 1,2,3 becomes 3efbe78a8d82f29979031a4aa0b16a9d.
    # 1,2,4 becomes 63960835bcdc130f0b66d7ff4f6a5a8e.

    with open(filename) as file:
        # newline allows us to test multiple datastreams in a testfile
        # the real input data has only one line
        for line in file:
            print("Processing line: '{}'".format(line.strip()))
            part2_process_line(line)

# print("------------------------------ PART 1 - START")
# part1()
# print("------------------------------ PART 1 - END")
print("------------------------------ PART 2 - START")
part2()
print("------------------------------ PART 2 - END")
