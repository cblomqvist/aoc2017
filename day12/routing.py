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

def probe(currentnode, all_nodes, visited):
    for connection_id in currentnode.connections:
        if connection_id not in visited:
            visited.append(connection_id)
            probe(all_nodes[connection_id], all_nodes, visited)

target_id = '0'
with open(filename) as file:
    nodes = process_input(file)
    target = nodes[target_id]
    visited = []
    probe(target, nodes, visited)
    connected = target.connections
    print("There are {} nodes connected to node {}, direct or indirect".format(len(visited), target_id))
