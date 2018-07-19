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
        self.weight = int(weight)
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
print("PART 1 :: Root node representation: {}".format(rootnode))

################################################################################
############# Additions for PART 2 begins
################################################################################

log.info("Looking for unbalanced sub tree...")

# Calculate weight of a branch
def calculate_branch_weight(node):
    if node.children == {}:
        log.info("Weigth of {} is {}".format(node.key, node.weight))
        return node.weight
    weight = node.weight
    for child in node.children:
        weight += calculate_branch_weight(node.children[child])
    return weight

def find_unbalance(node):
    # Counts how many nodes have the same weight
    log.info("Inspecting children of {}...".format(node))
    log.info("node is of type {}".format(type(node)))
    log.info("Inspecting {} children...".format(len(node.children)))
    children_by_weight = {}
    for branch in node.children:
        current_branch = node.children[branch]
        weight = calculate_branch_weight(current_branch)
        if weight in children_by_weight:
            children_by_weight[weight].append(current_branch)
        else:
            children_by_weight[weight] = [current_branch]
    
    oddone_list = [x for x in children_by_weight if len(children_by_weight[x]) == 1]
    if len(oddone_list) == 0:
        # We have balance here
        return None, 0
 
    # Unbalance detected
    odd_weight = oddone_list[0]
    # This list has ony one item: the odd child
    odd_child = children_by_weight[odd_weight][0]
    majority_weight = [x for x in children_by_weight if len(children_by_weight[x]) > 1][0]
    diff = majority_weight - odd_weight
    log.info("Unbalanced weight of '{}' is '{}', majority_weight: {}, diff: {} from branch: {}".format(
        node.key, odd_weight, majority_weight, diff, odd_child))

    # Look for unbalance among its children
    child_unbalance, child_diff = find_unbalance(odd_child)
    if child_unbalance != None:
        # Unbalance is higher up in tower, among children
        return child_unbalance, child_diff
    # No further unbalance detected so this is the unbalanced node    
    return odd_child, diff


unbalanced, diff = find_unbalance(rootnode)
print(unbalanced)
print(diff)
if unbalanced == None:
    print("The tree is balanced!")
else:
    expected_weight = unbalanced.weight + diff
    print("Correcting node '{}' from {} to {} would fix the imbalance".format(
        unbalanced.key, unbalanced.weight, expected_weight))
