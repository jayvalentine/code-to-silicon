class BasicBlock:
  def __init__(self, instructions):
    self._instructions = instructions

  def __str__(self):
    s = "Basic Block:\n"

    s += "\tInputs: " + ", ".join(list(map(
      lambda i: "r" + str(i),
      self.inputs()))) + "\n"

    s += "\tOutputs: " + ", ".join(list(map(
      lambda i: "r" + str(i),
      self.outputs()))) + "\n"

    s += "\tMemory-access Density: " + str(round(self.memoryAccessDensity(), 2)) + "\n"

    s += "Instructions:\n"
    for i in self._instructions:
      s += "\t" + str(i) + "\n"

    return s

  def __len__(self):
    return len(self._instructions)

  def instructions(self):
    return self._instructions

  def memoryAccessDensity(self):
    numInstructions = 0
    numMemoryAccess = 0

    for i in self._instructions:
      numInstructions += 1
      if i.isMemoryAccess():
        numMemoryAccess += 1

    return (float(numMemoryAccess)/float(numInstructions))

  def outputs(self):
    outputs = []

    for i in self._instructions:
      if i.rD() != None and i.rD() not in outputs:
        outputs.append(i.rD())

    if 0 in outputs:
      outputs.remove(0)

    return outputs

  def inputs(self):
    inputs = []

    outputs = []

    for i in self._instructions:
      if i.rA() != None and i.rA() not in inputs and i.rA() not in outputs:
        inputs.append(i.rA())

      if i.rB() != None and i.rB() not in inputs and i.rB() not in outputs:
        inputs.append(i.rB())

      if i.rD() != None and i.rD() not in outputs:
        outputs.append(i.rD())

    return inputs

def extractBasicBlocks(stream):
  blocks = []

  currentBlock = []

  for s in stream:
    if s.isInstruction():
      if s.isBasicBlockBoundary():
        blocks.append(BasicBlock(currentBlock))
        currentBlock = []
      else:
        currentBlock.append(s)
    else:
      blocks.append(BasicBlock(currentBlock))
      currentBlock = []

  blocks.append(BasicBlock(currentBlock))

  blocks = list(filter(lambda b: len(b) > 0, blocks))

  return blocks
