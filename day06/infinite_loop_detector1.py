import argparse
import logging

def setup(name = 'root'):
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

log = setup()

# This lets us parse argument from the command line
parser = argparse.ArgumentParser(description="Figure out number of cycles possible before we enter an infinite loop. See instructions.txt")

# We need to read a file
parser.add_argument("filename", help="The file to read")

# Let' see what we get from the command line
args = parser.parse_args()

filename = args.filename
log.info("The file to read is: {}".format(args.filename))

input = []
with open(filename) as file:
    for line in file:
        log.info("Read this line: '{}'".format(line))
        input = input + line.split()
        log.info("Input converted to: {}".format(input))

banks = []
for x in input:
    banks.append(int(x))
log.info("Initial state of memory banks: {}".format(input))


# Determine maximum value and find first bank with the maximum value
def find_start_bank(state):
    max = state[0]
    startindex = 0
    index = 0
    for i in state:
        if (max < i):
            max = i
            startindex = index
        index += 1
    log.debug("Start index for {} is: {}".format(state, startindex))
    return startindex


def redistribute(state):
    # Find bank to purge
    startbank = find_start_bank(state)
    remaining_blocks = state[startbank]
    state[startbank] = 0

    # Find out which index to start looping at
    startindex = startbank + 1
    startindex = 0 if startindex == len(state) else startindex

    # Reallocate memory blocks
    while remaining_blocks > 0:
        for i in range(startindex, len(state)):
            state[i] = state[i] + 1
            remaining_blocks -= 1
            if remaining_blocks == 0:
                break
        # Reset startindex in case we have more to redistribute
        startindex = 0

    return str(state)

states = set()
iterations = 0

print("Looking for infinite loop...")
while True:
    state = redistribute(banks)
    iterations += 1
    if iterations % 100 == 0:
        log.info("{} iterations. State: {}".format(iterations, state))
    if state in states:
        # We've seen this before so now we are entering the infinte loop
        print("Infinite loop detected at iteration {} !".format(iterations))
        break
    states.add(state)


