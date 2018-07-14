import argparse
import logtest

logger = logtest.setup()

def has_duplicates(words):
    for current_word in words:
        counter = 0
        for word in words:
            if (word == current_word):
                counter += 1
        if counter > 1:
            logger.info("The word '{}' was duplicated in {}".format(current_word, words))
            return True
    return False

def is_valid_passphrase(phrase):
    words = phrase.split(' ')
    if (len(words) < 2):
        return False
    if (has_duplicates(words)):
        return False
    logger.debug("VALID: '{}'".format(phrase))
    return True

# This lets us parse argument from the command line
parser = argparse.ArgumentParser(description="Count number of valid passphrases in a text file")

# We need to read a file
parser.add_argument("filename", help="The file to read")

# Let' see what we get from the command line
args = parser.parse_args()

filename = args.filename
logger.info("The file to read is: {}".format(args.filename))

valid_phrases = 0
with open(filename) as file:
    for line in file:
        if is_valid_passphrase(line.strip()):
            valid_phrases += 1
print("There are {} valid passphrases in '{}'".format(valid_phrases, filename))
