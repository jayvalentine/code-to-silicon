class StreamItem:
  def __init__(self):
    self._next = None

  def getNext(self):
    return self._next

  def setNext(self, next):
    self._next = next

  def isInstruction(self):
    return False