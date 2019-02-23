from parsing import instructions

class BasicBlock:
  def __init__(self, name, function):
    self._name = name

    if function == None:
      raise ValueError("Expected function name, got None.")

    self._function = str(function)

    self._instructions = {}
    self._prev = []
    self._next = []

  def __str__(self):
    s = "Basic Block: " + self._name + " in function " + self._function + "\n"

    s += "\tInputs: " + ", ".join(list(map(
      lambda i: "r" + str(i),
      self.inputs()))) + "\n"

    s += "\tOutputs: " + ", ".join(list(map(
      lambda i: "r" + str(i),
      self.outputs()))) + "\n"

    s += "\tUsed: " + ", ".join(list(map(
      lambda i: "r" + str(i),
      self.used()))) + "\n"

    s += "\tMemory-access Density: " + str(round(self.memoryAccessDensity(), 2)) + "\n"

    s += "\tPrevious blocks:\n"
    for b in self._prev:
      s += b.name() + " "

    s += "\tNext blocks:\n"
    for b in self._next:
      s += b.name() + " "

    s += "Instructions:\n"
    for l in sorted(list(self._instructions.keys())):
      s += "\t{:04d}: {:s}\n".format(l, str(self._instructions[l]))

    return s

  def __len__(self):
    return len(self._instructions)

  def add(self, line, instruction):
    if not isinstance(instruction, instructions.Instruction):
      raise TypeError("Not an instruction: " + str(instruction))

    if line in self._instructions.keys():
      raise ValueError("Duplicate line number " + str(line) + ": have " + str(self._instructions.keys()) + ", got " + str(instruction))

    self._instructions[line] = instruction

  def instructions(self):
    return self._instructions

  def memoryAccessDensity(self):
    numInstructions = 0
    numMemoryAccess = 0

    for l in self._instructions.keys():
      numInstructions += 1
      if self._instructions[l].isMemoryAccess():
        numMemoryAccess += 1

    return (float(numMemoryAccess)/float(numInstructions))

  def outputs(self):
    outputs = []

    for l in sorted(list(self._instructions.keys())):
      i = self._instructions[l]
      if i.rD() != None and i.rD() not in outputs:
        outputs.append(i.rD())

    if 0 in outputs:
      outputs.remove(0)

    return outputs

  def inputs(self):
    inputs = []

    outputs = []

    for l in sorted(list(self._instructions.keys())):
      i = self._instructions[l]
      if i.rA() != None and i.rA() not in inputs and i.rA() not in outputs:
        inputs.append(i.rA())

      if i.rB() != None and i.rB() not in inputs and i.rB() not in outputs:
        inputs.append(i.rB())

      if i.rD() != None and i.rD() not in outputs:
        outputs.append(i.rD())

    return inputs

  def used(self):
    used = []

    for l in sorted(list(self._instructions.keys())):
      i = self._instructions[l]
      if i.rA() != None and i.rA() not in used:
        used.append(i.rA())
      if i.rB() != None and i.rB() not in used:
        used.append(i.rB())
      if i.rD() != None and i.rD() not in used:
        used.append(i.rD())

    return used

def extractBasicBlocks(stream):
  blocks = []

  currentBlock = None
  currentFunction = None

  for i in range(len(stream)):
    s = stream[i]

    if s.isInstruction():
      if currentBlock == None:
        currentBlock = BasicBlock("nolabel-line-{:04d}".format(i), currentFunction)

      # If the instruction is a NOP and we're not already in the middle
      # of a basic block, ignore it and skip ahead.
      if type(s) is instructions.NOPInstruction and (len(currentBlock) == 0 or currentBlock == None):
        currentBlock = None
        continue

      currentBlock.add(i, s)
      if s.isBasicBlockBoundary():
        blocks.append(currentBlock)
        currentBlock = BasicBlock("nolabel-line-{:04d}".format(i), currentFunction)
    elif s.isLabel():
      if currentBlock != None:
        blocks.append(currentBlock)

      currentBlock = BasicBlock(s.name() + "-line-{:04d}".format(i), currentFunction)
    elif s.isDirective():
      if s.directive() == "type" and s.args(1) == "@function":
          currentFunction = s.args(0)

  if len(currentBlock) > 0:
    blocks.append(currentBlock)

  blocks = list(filter(lambda b: len(b) > 0, blocks))

  return linkBasicBlocks(blocks)

def linkBasicBlocks(blocks):
  for i in range(len(blocks)):
    # A basic block can be linked to another in one of two ways:
    # 1. a branch instruction
    # 2. a return
    #
    # We can always know the label to which we're jumping (as it's in the instruction itself),
    # but we might not always know where we're returning to (e.g. if the call site is in another compilation unit.)
    pass

  return blocks
