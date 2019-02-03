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

def prettyPrint(stream):
  for s in stream:
    if s.isInstruction():
      print("\t" + str(s))
    else:
      print(s)

def parseStreamItems(stream):
  # Check the list is the right length.
  if len(stream) < 1:
    raise ValueError("Must provide at least one instruction for parsing.")

  streamItems = []

  for line in stream:
    streamItems.append(parseStreamItem(line))

  return streamItems

def parseStreamItem(streamItem):
  # Is this a label? If so, parse as a label.
  if streamItem[-1] == ":":
    return labels.parseLabel(streamItem)
  else:
    return instructions.parseInstruction(streamItem)