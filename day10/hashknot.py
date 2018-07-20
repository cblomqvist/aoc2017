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
    def __init__(self, list):
        for i in range(0,256):
            self.list.add(i)
        self.size = len(self.list)
        self.pos = 0
        self.skipsize = 0
    
    def __str__(self):
        return str(list)
    
    def __repr__(self):
        return self.__str__(self)

    def twist(self, length):
        # Create a sub-list starting at self.pos with length = length, 
        # possibly wrapping past position 255.

        # Reverse that sub-list

        # Replace section in self.list with the sub-list
    
        # Increase pos by length + self.skipsize

        # Increase self.skipsize by 1 for the next round

