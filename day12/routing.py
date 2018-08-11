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

class Node:
    def __init__(self, id, connections):
        self.id = id
        self.connections = connections
        self.group = None
    
    def __str__(self):
        return "{} - {}".format(self.id, self.connections)

    def __repr__(self):
        return self.__str__()

def process_input(input):
    nodes = {}
    for line in input:
        data = line.strip().split(' <-> ')
        log.debug("Data: {}".format(data))
        id = data[0]
        log.debug("id: {}".format(id))
        connections = data[1].split(', ')
        log.debug("connections: {}".format(connections))
        node = Node(id, connections)
        log.debug("Node: {}".format(node))
        nodes[id] = node
    return nodes

def probe(currentnode, all_nodes, visited, group_id):
    currentnode.group = group_id
    for connection_id in currentnode.connections:
        if connection_id not in visited:
            visited.append(connection_id)
            next_node = all_nodes[connection_id]
            probe(next_node, all_nodes, visited, group_id)

with open(filename) as file:
    log.info("Processing {}...".format(filename))
    nodes = process_input(file)
    log.info("The file {} contained {} nodes.".format(filename, len(nodes)))
    group_id = 0
    for target_id in nodes:
        target = nodes[target_id]
        if target.group is None:
            group_id += 1
            log.info("Node {} is starting a new group: {}".format(target_id, group_id))
            visited = []
            probe(target, nodes, visited, group_id)
            connected = target.connections
            print("There are {} nodes connected to node {}, direct or indirect".format(len(visited), target_id))
    print("There are {} groups in total!".format(group_id))


