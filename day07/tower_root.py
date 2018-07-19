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

# The Node class will represent nodes in the "balanced" tree that is the tower
class Node:
    def __init__(self, key, weight):
        self.key = key
        self.weight = weight
        self.children = {}
        self.parent = None

    def __str__(self):
        return "{} ({}) -> {} (parent: {})".format(self.key, self.weight, len(self.children), self.parent.key if self.parent != None else "none")

    def __repr__(self):
        return self.__str__()

    # Add a Node as a child to this Node
    def add(self, node):
        self.children[node.key] = node
        node.parent = self

    # Find out if there is a Node with the same name somewhere in the tree already
    def find(self, key):
        if key in self.children:
            return self.children[key]
        for child in self.children:
            res = child.find(key)
            if res != None:
                return res
        return None

def node_by_weight(line):
    # We have a line in the format 'ktlj (57)'
    data = line.split(' ')
    key = data[0]
    weight = data[1][1:-1]
    return Node(key, weight)

def node_from_line(line):
    log.info("Processing '{}'".format(line))
    if " -> " not in line:
        return node_by_weight(line)
    else:
        return node_by_weight(line.split("->")[0].strip())
    log.error("Line '{}' was skipped as support for it is not yet implemented!".format(line))
    return None

def get_parent(nodes, line):
    parts = line.split(" -> ")
    key = parts[0].split()[0]
    parent = nodes[key]
    return parent

def add_children(nodes, line):
    if " -> " not in line:
        return
    parent = get_parent(nodes, line.strip())
    parts = line.split(" -> ")
    children = parts[1].strip().split(", ")
    log.info("Adding children {} to {}".format(children, parent))
    for child in children:
        childnode = nodes[child]
        parent.add(childnode)
        log.info("Parent status: {}".format(parent))

# Collect nodes in lists by the number of children
nodes = {}
with open(filename) as file:
    for line in file:
        node = node_from_line(line.strip())
        nodes[node.key] = node
with open(filename) as file:
    for line in file:
        add_children(nodes, line)

def find_root(nodes):
    return [node for node in nodes if nodes[node].parent == None]

print(nodes)

rootlist = find_root(nodes)
print("Root node list (should be one element): {}".format(rootlist))

rootnode = nodes[rootlist[0]]
print("Root node representation: {}".format(rootnode))
