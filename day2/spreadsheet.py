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

def calculate_line_checksum_max_min_diff(line):
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

def calculate_file_checksum_max_min_diff_of_file(filename):
    checksum = 0
    with open(filename) as file:
        for line in file:
            linesum = calculate_line_checksum_max_min_diff(line.rstrip('\n'))
            # print("Linesum of '{}' is {}".format(line.rstrip('\n'), linesum))
            checksum += linesum

    print("File max-min Checksum of {} is {}".format(filename, checksum))

calculate_file_checksum_max_min_diff_of_file(args.filename)

def calculate_line_checksum_even_division(line):
    cells = line.split()
    # we only need to find the first case where division succeeds
    for i in range(len(cells)):
        first = int(cells[i])
        the_rest = cells[i+1:len(cells)]
        for j in range(len(the_rest)):
            second = int(the_rest[j])
            if (first % second == 0):
                return first / second
            if (second % first == 0):
                return second / first
            
def calculate_file_even_division_of_file(filename):
    checksum = 0
    with open(filename) as file:
        for line in file:
            linesum = calculate_line_checksum_even_division(line.rstrip('\n'))
            # print("Linesum of '{}' is {}".format(line.rstrip('\n'), linesum))
            checksum += linesum

    print("File max-min Checksum of {} is {}".format(filename, checksum))

calculate_file_even_division_of_file(args.filename)
