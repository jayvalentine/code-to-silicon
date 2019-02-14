class TextWriter:
  def __init__(self, tabWidth):
    self._str = ""

    self._commentLeader = ""
    self._indentationChar = " "
    self._tabWidth = tabWidth
    self._indentation = 0

  def __str__(self):
    return self._str

  def indent(self):
    return self._indentationChar * (self._tabWidth * self._indentation)

  def increaseIndent(self):
    self._indentation += 1

  def decreaseIndent(self):
    self._indentation -= 1

  def writeLine(self, s):
    self._str += self.indent() + s + "\n"

  def writeBlankLine(self):
    self.writeLine("")
