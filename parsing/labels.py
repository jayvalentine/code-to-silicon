from . import streams

class Label(streams.StreamItem):
  def __init__(self, labelName):
    self._labelName = str(labelName)

    super(Label, self).__init__()

  def __str__(self):
    return self._labelName + ":"

def parseLabel(labelString):
  labelString = str(labelString)

  if len(labelString) < 2:
    raise ValueError(labelString + " is not a valid label: wrong length.")

  if labelString[-1] != ":":
    raise ValueError(labelString + " is not a valid label: missing colon.")

  return Label(labelString[:-1])