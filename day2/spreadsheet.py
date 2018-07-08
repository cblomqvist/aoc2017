import argparse
import logging

# This lets us parse argument from the command line
parser = argparse.ArgumentParser(description="Calculate chacksum of a spreadsheet, ascii text with space separated columns.")

# We need to read the spreadsheet file to calculate checksums from
parser.add_argument("filename", help="The spreadsheet file to read")

# Let' see what we get from the command line
args = parser.parse_args()

logging.info("LOG The file to read is: {}".format(args.filename))
print("PRINT The file to read is: {}".format(args.filename))

def calculate_line_checksum(line):
    first = True
    min = 0
    max = 0
    for cell in line.split():
        number = int(cell)
        if (first):
            min = number
            max = number
            first = False
        else:
            if (min > number):
                min = number
            if (max < number):
                max = number
    return max - min

checksum = 0
with open(args.filename) as file:
    for line in file:
        linesum = calculate_line_checksum(line.rstrip('\n'))
        print("Linesum of '{}' is {}".format(line.rstrip('\n'), linesum))
        checksum += linesum

print("Checksum of {} is {}".format(args.filename, checksum))
