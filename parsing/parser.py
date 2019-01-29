from instruction import *

"""
Gets a list of instructions (as strings) and parses them into internal representation.

Parameters:
  - instructions - list of instructions (must be at least length 1) to be parsed.

Raises:
  - ValueError if instruction list is of length 0.
"""
def parse(instructions):
  # Check the list is the right length.
  if len(instructions) < 1:
    raise ValueError("Must provide at least one instruction for parsing.")

  # Get the first instruction, and convert into internal representation.
  instructionString = instructions[0]
  firstInstruction = parseInstruction(instructionString)

  # Get the rest of the instructions.
  otherInstructions = instructions[1:-1]

  # Parse the next instruction recursively, setting up the linked list as we go.
  firstInstruction.setNext(parse(otherInstructions))

  return firstInstruction