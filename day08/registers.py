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

INDEX_REGISTRY = 0
INDEX_OPERATION = 1
INDEX_ARGUMENT = 2
# Index 3 i salways 'if'
INDEX_LEFT_CONDITION = 4
INDEX_CONDITION = 5
INDEX_RIGHT_CONDITION = 6

registrys = {}

def get_reg_name(instruction):
    return instruction.strip().split(" ")[INDEX_REGISTRY]

def get_operation_name(instruction):
    return instruction.strip().split(" ")[INDEX_OPERATION]

def get_argument(instruction):
    return int(instruction.strip().split(" ")[INDEX_ARGUMENT])

def get_registry_value(key):
    value = int(registrys.get(key, 0))
    return value

# Max value ever held in any registry
maximum_value_ever = None
maximum_value_key = None

def set_registry_value(key, value):
    global maximum_value_ever
    global maximum_value_key
    registrys[key] = value
    if maximum_value_ever == None or maximum_value_ever < value:
        maximum_value_ever = value
        maximum_value_key = key

def get_left_condition(instruction):
    key = instruction.strip().split(" ")[INDEX_LEFT_CONDITION]
    return get_registry_value(key)

def get_right_condition(instruction):
    return int(instruction.strip().split(" ")[INDEX_RIGHT_CONDITION])

def get_condition(instruction):
    return instruction.strip().split(" ")[INDEX_CONDITION]

def eq(a, b):
    return a == b

def neq(a, b):
    return a != b

def gt(a, b):
    return a > b

def gte(a, b):
    return a >= b

def lt(a, b):
    return a < b

def lte(a, b):
    return a <= b

# Example: b inc 5 if a > 1
# Condition is here: a > 1

condition_switcher = {
    "==": eq,
    "!=": neq,
    ">": gt,
    ">=": gte,
    "<": lt,
    "<=": lte
}

def eval_condition(instruction):
    # Get value of registry 'a'
    left = get_left_condition(instruction)
    # Get value to compare to ('1' in the example):
    right = get_right_condition(instruction)
    # Apply comparison to 1
    condition = get_condition(instruction)
    # Lookup function to call from condition_switcher
    func = condition_switcher.get(condition, lambda: "Invalud condition: '{}'".format(condition))
    # Call the function
    return func(left, right)

def inc(a,b):
    return a + b

def dec(a,b):
    return a - b

operation_switcher = {
    "inc": inc,
    "dec": dec
}

def apply_instruction(instruction):
    if eval_condition(instruction):
        log.info("Applying instruction '{}'".format(instruction))
        target_registry = get_reg_name(instruction)
        argument = get_argument(instruction)
        operation = get_operation_name(instruction)
        # Lookup function to call from operation_switcher
        func = operation_switcher.get(operation, lambda: "Invalud operation: '{}'".format(operation))
        # Call the function
        registry_value = get_registry_value(target_registry)
        result = func(registry_value, argument)
        set_registry_value(target_registry, result)
    else:
        log.info("Skipping instruction '{}'".format(instruction))


with open(filename) as file:
    for line in file:
        instruction = line.strip()
        apply_instruction(instruction)

largest = None
regkey = None
for key in registrys:    
    value = get_registry_value(key)
    if largest == None:
        largest = value
        regkey = key
        continue
    if value > largest:
        largest = value
        regkey = key
    
print("The largest registry value I found was {} in registry '{}'".format(largest, regkey))
print("The largest registry value ever was {} in registry '{}'".format(maximum_value_ever, maximum_value_key))