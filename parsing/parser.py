from . import instructions

class Label:
  def __init__(self, labelName, instructionHead):
    self._labelName = str(labelName)

    if instructionHead == None:
      raise ValueError("Attempt to initialize label " + labelName + " with an empty instruction list.")

    self._instructionHead = instructionHead

  def __str__(self):
    s = self._labelName + ":\t" + str(self._instructionHead) + "\n"

    i = self._instructionHead.getNext()
    while i != None:
      s += "\t" + str(i) + "\n"
      i = i.getNext()

    return s[0:-1]

def parse(stream):
  # Strip all leading/trailing whitespace from lines.
  stream = list(map(lambda l: l.strip(), stream))

  # Find the locations of all labels.
  labelIndexList = []

  for line in stream:
    # Yes, I know. This is an incredibly naive way of seeing if something is
    # a label. But it might just work.
    if line[-1] == ':':
      labelIndexList.append(stream.index(line))

  blocks = []

  # We now have a list of indices of labels, so we should
  # be able to split the stream up into blocks.
  for i in range(len(labelIndexList)-1):
    blocks.append(stream[labelIndexList[i]:labelIndexList[i+1]])

  labels = []

  for block in blocks:
    labels.append(Label(block[0][:-1], parseInstructions(block[1:])))

  return labels

"""
Gets a list of instructions (as strings) and parses them into internal representation.

Parameters:
  - instructions - list of instructions (must be at least length 1) to be parsed.

Raises:
  - ValueError if instruction list is of length 0.
"""
def parseInstructions(instructionList):
  # Check the list is the right length.
  if len(instructionList) < 1:
    raise ValueError("Must provide at least one instruction for parsing.")

  # Get the first instruction, and convert into internal representation.
  instructionString = instructionList[0]
  firstInstruction = instructions.parseInstruction(instructionString)

  # Get the rest of the instructions.
  otherInstructions = instructionList[1:]

  if len(otherInstructions) > 0:
    # Parse the next instruction recursively, setting up the linked list as we go.
    firstInstruction.setNext(parseInstructions(otherInstructions))

  return firstInstruction
