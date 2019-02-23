from parsing import instructions

class BasicBlock:
  def __init__(self, name, function, label):
    self._name = name

    if function == None:
      raise ValueError("Expected function name, got None.")

    self._function = str(function)

    self._label = label

    self._instructions = {}
    self._prev = []
    self._next = []

    self._unknownNext = False
    self._unknownPrev = False

  def __str__(self):
    s = "Basic Block: " + self._name + " in function " + self._function

    if self._label != None:
      s += " (label: " + self._label + ")"

    s += "\n"

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

    s += "\tPrevious blocks:"
    for b in self._prev:
      s += b.name() + " "

    if self._unknownNext:
      s += "(unknown)"

    s += "\n"

    s += "\tNext blocks:"
    for b in self._next:
      s += b.name() + " "

    if self._unknownPrev:
      s += "(unknown)"

    s += "\n"

    s += "Instructions:\n"
    for l in sorted(list(self._instructions.keys())):
      s += "\t{:04d}: {:s}\n".format(l, str(self._instructions[l]))

    return s

  def __len__(self):
    return len(self._instructions)

  def name(self):
    return self._name

  def function(self):
    return self._function

  def label(self):
    return self._label

  def last(self):
    lastLine = sorted(list(self._instructions.keys()))[-1]
    return self._instructions[lastLine]

  def add(self, line, instruction):
    if not isinstance(instruction, instructions.Instruction):
      raise TypeError("Not an instruction: " + str(instruction))

    if line in self._instructions.keys():
      raise ValueError("Duplicate line number " + str(line) + ": have " + str(self._instructions.keys()) + ", got " + str(instruction))

    self._instructions[line] = instruction

  def addNext(self, otherBlock):
    self._next.append(otherBlock)
    otherBlock._prev.append(self)

  def addUnknownNext(self):
    self._unknownNext = True

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

def extractBasicBlocks(logger, stream):
  blocks = []

  currentBlock = None
  currentFunction = None

  for i in range(len(stream)):
    s = stream[i]

    if s.isInstruction():
      if currentBlock == None:
        currentBlock = BasicBlock("nolabel-line-{:04d}".format(i), currentFunction, None)

      # If the instruction is a NOP and we're not already in the middle
      # of a basic block, ignore it and skip ahead.
      if type(s) is instructions.NOPInstruction and (len(currentBlock) == 0 or currentBlock == None):
        currentBlock = None
        continue

      currentBlock.add(i, s)
      if s.isBasicBlockBoundary():
        blocks.append(currentBlock)
        currentBlock = BasicBlock("nolabel-line-{:04d}".format(i), currentFunction, None)
    elif s.isLabel():
      if currentBlock != None:
        blocks.append(currentBlock)

      currentBlock = BasicBlock(s.name() + "-line-{:04d}".format(i), currentFunction, s.name())
    elif s.isDirective():
      if s.directive() == "type" and s.args(1) == "@function":
          currentFunction = s.args(0)

  if len(currentBlock) > 0:
    blocks.append(currentBlock)

  blocks = list(filter(lambda b: len(b) > 0, blocks))

  return linkBasicBlocks(logger, blocks)

def linkBasicBlocks(logger, blocks):
  for i in range(len(blocks)):
    # A basic block can be linked to another in one of two ways:
    # 1. a branch instruction
    # 2. a return
    #
    # We can always know the label to which we're jumping (as it's in the instruction itself),
    # but we might not always know where we're returning to (e.g. if the call site is in another compilation unit.)
    
    b = blocks[i]

    # We should never see a basic block which doesn't end with a control flow instruction.
    lastInstruction = b.last()
    if not lastInstruction.isBasicBlockBoundary():
      raise ValueError("Expected control flow instruction as end of block " + b.name() + ", got " + str(lastInstruction))

    # If this is a normal branch instruction, find the block we're branching to.
    if lastInstruction.isBranch():
      branchLabel = lastInstruction.label()

      blocksWithLabel = list(filter(lambda b: b.label() == branchLabel, blocks))

      if len(blocksWithLabel) > 1:
        raise ValueError("Label " + branchLabel + " is ambiguous (" + str(len(blocksWithLabel)) + " matches)")
      elif len(blocksWithLabel) < 1:
        logger.warn("Unknown label: " + branchLabel)
        b.addUnknownNext()
      else:
        b.addNext(blocksWithLabel[0])

    elif lastInstruction.isReturn():
      # Get the name of the function this block is in.
      currentFunction = b.function()


  return blocks
