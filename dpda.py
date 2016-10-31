#!/usr/bin/python

# Imports
# =============================================================================

import getopt
import sys
import os

# Global variables
# =============================================================================

PROGRAM_NAME    = os.path.basename(sys.argv[0])
DEF_FILE        = ''
TEST_FILE       = ''

# Functions
# =============================================================================

def error(message, exit_code = 1):
    print >>sys.stderr, message
    sys.exit(exit_code)

def usage(exit_code = 0):
    error('''Usage: {} [ -h ] DPDA_DEFINITION_FILE TEST_STRING_FILE

    Options:

        -h Show this help message'''
        .format(PROGRAM_NAME, exit_code))

# Parse command line arguments
# =============================================================================

try:
    options, arguments = getopt.getopt(sys.argv[1:], "h")
except getopt.GetoptError as e:
    error(e)

for option, value in options:
    if option == '-h':
        usage(0)
    else:
        usage(1)

if len(arguments) < 2 or len(arguments) > 2:
    usage(1)
else:
    DEF_FILE = arguments[0]
    TEST_FILE = arguments[1]

# Main Execution
# =============================================================================

# Open the FA machine defition file and load its contents
with open(DEF_FILE) as f:
    definition_lines = f.readlines()
# Strip the trailing whitespace from each line in the def file
for i in range(len(definition_lines)):
    definition_lines[i] = definition_lines[i].rstrip()

# Print the machine name
print definition_lines[0]

# Parse the rest of the machine defition
# ----------------------------------------------------------------------------

input_alphabet = definition_lines[1].split(",")
# Check if "~" is in the input alphabet
if "~" in input_alphabet:
    error("The character \"~\" not allowed in the input alphabet.")

stack_alphabet = definition_lines[2].split(",")
# Check if "~" is in the stack alphabet
if "~" in stack_alphabet:
    error("The character \"~\" not allowed in the stack alphabet.")

states = definition_lines[3].split(",")
start_state = definition_lines[4]
accepting_states = definition_lines[5].split(",")
rules = definition_lines[6:]

# Print the rules with associated rule number
rule_n = 0
for rule in rules:
    rule_n = rule_n + 1
    print "{}: {}".format(rule_n, rule)

# Print the name of the test file
print "Test File: {}".format(TEST_FILE)
# Open the FA test file and load its contents
with open(TEST_FILE) as f:
    input_lines = f.readlines()
# Strip the trailing whitespace from each line in the test file
for i in range(len(input_lines)):
    input_lines[i] = input_lines[i].rstrip()

# Loop over each of the test strings
for line in input_lines:
    print "String: {}".format(line) # Print the test string
    transitions = list(line) # Split the test string up
    next_state = start_state
    stack = []
    step = 0

    # Loop over each of the transitions in the test string
    for transition in transitions:
        curr_state = next_state
        next_state = None
        step = step + 1
        rule_n = 0

        # First, follow epsilon rules
        for rule in rules:
            rule = rule.split(",")
            rule_n = rule_n + 1
            if rule[0] == curr_state and rule[1] == "~":
                top = (rule[2].split("|"))[0]
                if (len(stack) is not 0 and (top == stack[len(stack)-1] or top == "~")) or (len(stack) is 0 and top == "~"):
                    next_state = (rule[2].split("|"))[1]
                if len(stack) is not 0 and not top == "~":
                    stack.pop()
                if not rule[3] == "~":
                    stack.append(rule[3])
                print "{}#{}: {},{},{}|{},{}".format(step, rule_n,
                    curr_state, "~", top, next_state, rule[3])
                curr_state = next_state
                next_state = None
                step = step + 1

        # Then, find a matching rule for the transition character
        rule_n = 0
        for rule in rules:
            rule = rule.split(",")
            rule_n = rule_n + 1
            if rule[0] == curr_state and rule[1] == transition:
                top = (rule[2].split("|"))[0]
                if (len(stack) is not 0 and (top == stack[len(stack)-1] or top == "~")) or (len(stack) is 0 and top == "~"):
                    next_state = (rule[2].split("|"))[1]
                    if len(stack) is not 0 and not top == "~":
                        stack.pop()
                    if not rule[3] == "~":
                        stack.append(rule[3])
                    print "{}#{}: {},{},{}|{},{}".format(step, rule_n,
                        curr_state, transition, top, next_state, rule[3])
                    break

        if next_state is None:
            break

    if next_state in accepting_states:
        print "Accepted"
    else:
        print "Rejected"
