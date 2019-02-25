from . import streams

class Directive(streams.StreamItem):
  def __init__(self, directive, args):
    self._directive = str(directive)
    self._args = args

  def __str__(self):
    return "." + self._directive + " " + ",".join(self._args)

  def isDirective(self):
    return True

  def directive(self):
    return self._directive

  def args(self, index):
    if index < 0 or index >= len(self._args):
      raise IndexError("Directive argument index out of range.")

    return self._args[index]

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

  directiveSplit = directiveString[1:].split()

  directive = directiveSplit[0]

  if len(directiveSplit) > 1:
    # We might have some spaces which means we will have accidentally split up our arg string.
    # Join it again so that it's just comma-separated.
    argString = "".join(directiveSplit[1:])
    args = list(map(lambda a: a.strip(), argString.split(",")))
  else:
    args = []

  return Directive(directive, args)
