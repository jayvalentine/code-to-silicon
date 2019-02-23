from . import streams, instructions, labels, directives

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

  # Strip any blank lines.
  stream = list(filter(lambda l: len(l) > 0, stream))

  # Strip any lines which are just comments.
  stream = list(filter(lambda l: l[0] != '#', stream))

  return parseStreamItems(stream)

def prettyPrint(stream):
  for s in stream:
    if s.isInstruction():
      print("\t" + str(s))
    else:
      print(s)

def parseStreamItems(stream):
  s = streams.Stream()

  # Check the list is the right length.
  if len(stream) < 1:
    raise ValueError("Must provide at least one instruction for parsing.")

  for line in stream:
    s.add(parseStreamItem(line))

  return s

def parseStreamItem(streamItem):
  # Is this a label? If so, parse as a label.
  if streamItem[-1] == ":":
    return labels.parseLabel(streamItem)
  # Is this a directive? If so, parse as a directive.
  if streamItem[0] == ".":
    return directives.parseDirective(streamItem)
  # Otherwise assume it's an instruction.
  else:
    return instructions.parseInstruction(streamItem)