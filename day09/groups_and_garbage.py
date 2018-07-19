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

class State:
    def __init__(self):
        self.group_starts = 0
        self.group_ends = 0
        self.score = 0
        self.is_garbage = False
        self.is_ignoring = False
        self.num_garbage_chars = 0

def is_garbage_start(char):
    return char == '<'
def is_garbage_end(char):
    return char == '>'
def is_group_start(char):
    return char == '{'
def is_group_end(char):
    return char == '}'
def is_ignore_char(char):
    return char == '!'

def process_stream(stream):
    state = State()

    for char in stream:
        if state.is_garbage:
            # Should we ignore this or the next char?
            if state.is_ignoring:
                # Ignore this one but not the next one
                state.is_ignoring = False
                continue
            elif is_ignore_char(char):
                # Ignore the next char
                state.is_ignoring = True
                continue
            # Since we are in garbage and not ignoring we are only interested in a garbage end char
            if is_garbage_end(char):
                state.is_garbage = False
                continue
            # This is a garbage character that we should "remove" so we count it as removed         
            state.num_garbage_chars += 1
            continue
        # Are we entering garbage?
        if is_garbage_start(char):
            state.is_garbage = True
            continue

        # Are we entering a data group?
        if is_group_start(char):
            state.group_starts += 1
            continue

        # Are we in a data group already
        if state.group_starts > 0:
            if is_group_end(char):
                # A completed group will up our score
                state.score += state.group_starts
                state.group_starts -= 1
                continue
    if len(stream) > 100:
        print("Your score for this stream is: {}, with {} garbage chars removed".format(state.score, state.num_garbage_chars))
    else:
        # Test streams are much shorter
        print("Your score for '{}' is: {}, with {} garbage chars removed".format(
            stream, state.score, state.num_garbage_chars))


with open(filename) as file:
    # newline allows us to test multiple datastreams in a testfile
    # the real input data has only one line
    linecounter = 1
    for line in file:
        # Char by char then process the data to find groups and scores
        if 'test' in filename:
            # The test file is split up to have test data followed by '#' and then a descrition of the test data
            print("Line {}: {}".format(linecounter, line.strip().split("#")[1].strip()))
            process_stream(line.strip().split("#")[0])
            linecounter += 1
        else:
            process_stream(line.strip())
