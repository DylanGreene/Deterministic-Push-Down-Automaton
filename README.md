Deterministic Push Down Automaton (DPDA) Simulator
==================================================

Written by: Dylan Greene  
Updated on: 31 October 2016

To run the simulator, ensure that dpda.py is executable. To ensure this, simply
run the command 'chmod +x dfa.py'.

The simulator must be run with a DPDA definition file which follows the
following format:
  * Line 1: The name of the DPDA program. This should be echoed to stdout
  before the rules are echoed.
  * Line 2: The set of symbols to be used for the input alphabet ∑: only single
  ASCII letters are allowed, comma separated, as in a,b,c,… "~" is not allowed
  as an alphabet character.
  * Line 3: The set of symbols to be used for the stack alphabet Γ: only single
  ASCII letters are allowed, comma separated, as in a,b,c,… "~" is not allowed
  as an alphabet character.
  * Line 4: The names of the states, separated by commas, as in q0,q1,… There
  is no constraint on the length of a state name.
  * Line 5: The name of the state that should be considered the start state.
  * Line 6: A comma separated list of state names that should be marked as
  accepting states.
  * Line 7 and beyond: one transition rule per line, in the format:
   \<Initial\_State\_Name\>,\<Input\_Symbol\>,\<stack_top\>|\<New\_State\_Name\>,\<new_stack_top>
Processing of rules stops with the end of file.

Note: "~" is used in both input and output to represent "ε".

Additionally, an test file containing the the character strings to run against
the machine must be supplied. The format for the test file is simply one line
for each string to be input to the machine.

To run the simulator with these two files, execute the command './dfa.py
DPDA_DEFINITION_FILE TEST_STRING_FILE'. A help message will be displayed if
usage is incorrect.

Once run, the simulator will print the transitions for every string, as
well as if each string is accepted or rejected by the machine.
