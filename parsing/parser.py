from . import instructions, labels

"""
Parse a stream of instructions and labels into a linked list of stream items (instructions and labels).

Parameters:
  - stream - list of strings representing instructions and labels.

Returns:
  - the head of the linked list of StreamItem objects.
"""
def parse(stream):
  # Strip all leading/trailing whitespace from lines.
  stream = list(map(lambda l: l.strip(), stream))

  return parseStreamItems(stream)

def prettyPrint(streamItem):
  if streamItem == None:
    return

  if streamItem.isInstruction():
    print("\t" + str(streamItem))
  else:
    print(streamItem)

  prettyPrint(streamItem.getNext())


def parseStreamItems(stream):
  # Check the list is the right length.
  if len(stream) < 1:
    raise ValueError("Must provide at least one instruction for parsing.")

  # Get the first instruction, and convert into internal representation.
  instructionString = stream[0]
  firstStreamItem = parseStreamItem(instructionString)

  # Get the rest of the instructions.
  otherStreamItems = stream[1:]

  if len(otherStreamItems) > 0:
    # Parse the next instruction recursively, setting up the linked list as we go.
    firstStreamItem.setNext(parseStreamItems(otherStreamItems))

  return firstStreamItem

def parseStreamItem(streamItem):
  # Is this a label? If so, parse as a label.
  if streamItem[-1] == ":":
    return labels.parseLabel(streamItem)
  else:
    return instructions.parseInstruction(streamItem)