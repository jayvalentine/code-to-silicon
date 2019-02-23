from . import streams

class Directive(streams.StreamItem):
  def __init__(self, directive, args):
    self._directive = str(directive)
    self._args = args

  def __str__(self):
    return "." + self._directive + " " + " ".join(self._args)

  def isDirective(self):
    return True

def parseDirective(directiveString):
  # Sanitise the input slightly. We don't care about comments.
  # These begin with a '#' and start after the end of the directive.
  if '#' in directiveString:
    directiveString = directiveString[:directiveString.index('#')]

  # Strip any leading and trailing whitespace.
  directiveString = directiveString.strip()
  directiveString = str(directiveString)

  if len(directiveString) < 2:
    raise ValueError(directiveString + " is not a valid directive: wrong length.")

  if directiveString[0] != ".":
    raise ValueError(directiveString + " is not a valid directive: does not start with '.'.")

  directiveSplit = directiveString.split(" ")

  directive = directiveString[0]
  args = directiveString[1].split(",")

  return Directive(directive, args)