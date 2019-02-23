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
        s += "    " + str(item)
      s += "\n"

    return s[:-1]

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
