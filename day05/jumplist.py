import argparse
import mylog

log = mylog.setup()

# This lets us parse argument from the command line
parser = argparse.ArgumentParser(description="Figure out number of jumps to excape the list in input.txt. See instructions.txt")

# We need to read a file
parser.add_argument("filename", help="The file to read")

# Let' see what we get from the command line
args = parser.parse_args()

filename = args.filename
log.info("The file to read is: {}".format(args.filename))

jumplist = []
with open(filename) as file:
    # Populate the jumplist with values
    for line in file:
        jumplist.append(int(line.strip()))

# Process the jumplist
index = 0
jumps = 0
# We are going to bounce around the list until we have exited it, i.e. gotten to an index outside of the jumplist
while index >= 0 and index < len(jumplist):
    nextindex = index + jumplist[index]
    jumps += 1
    jumplist[index] = 1 + jumplist[index]
    index = nextindex

print("The jumplist of {} steps was cleared in {} jumps and landed you on index {}.".format(len(jumplist), jumps, index))
