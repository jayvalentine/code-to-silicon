class StreamItem:
  def __init__(self):
    pass

  def isInstruction(self):
    return False

  def isLabel(self):
    return False

  def isDirective(self):
    return False

class Stream:
  def __init__(self):
    self._items = []

  def __str__(self):
    s = ""

    for item in self._items:
      if item.isLabel():
        s += str(item)
      else:
        s += "\t" + str(item)
      s += "\n"

    return s

  def __len__(self):
    return len(self._items)

  def __getitem__(self, index):
    return self._items[index]

  def add(self, item):
    if not isinstance(item, StreamItem):
      raise TypeError("Object of type " + str(type(item)) + " cannot be added to a stream.")

    self._items.append(item)

  def instructionCount(self):
    instructions = 0

    for item in self._items:
      if item.isInstruction():
        instructions += 1

    return instructions

  def labelCount(self):
    labels = 0

    for item in self._items:
      if item.isLabel():
        labels += 1

    return labels

  def directiveCount(self):
    directives = 0

    for item in self._items:
      if item.isDirective():
        directives += 1

    return directives

  def replaceLines(self, start, end, instructions):
    # Check that all the lines we're about to replace are:
    # a. in the stream
    # b. are instructions.
    startLen = len(self._items)

    if start >= len(self._items) or start < 0:
      raise IndexError("Start index is out of range.")
    if end >= len(self._items) or end < 0:
      raise IndexError("End index is out of range.")

    for l in range(start, end+1):
      if not self._items[l].isInstruction():
        raise ValueError("Specified range ({:d}, {:d}) is not a contiguous block of instructions.".format(start, end))

    # If we've got here without raising an error, it must be safe to slice!
    self._items[start:end+1] = instructions

    # Return the number of lines added or subtracted from the total length.
    return len(self._items) - startLen
