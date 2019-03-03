from parsing import instructions

class BasicBlock:
  def __init__(self, name, function, label):
    self._name = name

    if function == None:
      raise ValueError("Expected function name, got None.")

    self._function = str(function)

    self._label = label

    self._instructions = {}

    self._last = None
    self._lastLine = None

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

    s += "\tPrevious blocks: "
    for b in self._prev:
      s += b.name() + ", "

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

  def __getitem__(self, key):
    if key not in self._instructions.keys():
      raise KeyError("Line " + str(key) + " not in this basic block.")

    return self._instructions[key]

  def __len__(self):
    return len(self._instructions)

  def name(self):
    return self._name

  def function(self):
    return self._function

  def label(self):
    return self._label

  def setLast(self, line, instruction):
    self._last = instruction
    self._lastLine = line

  def splitAtLine(self, line):
    if line not in self._instructions.keys():
      raise KeyError("Cannot split at line " + str(line) + " as it is not in block" + self._name + ".")

    firstBlock = BasicBlock(self._name, self._function, self._label)
    secondBlock = BasicBlock("nolabel_line{:04d}".format(line), self._function, None)

    if self.last() != None:
      secondBlock.setLast(self.lastLine(), self.last())

    for l in self.lines():
      if l < line:
        firstBlock.add(l, self._instructions[l])
      else:
        secondBlock.add(l, self._instructions[l])

    return [firstBlock, secondBlock]

  def last(self):
    return self._last

  def lastLine(self):
    if self._lastLine == None:
      raise ValueError("Last line of block not set.")

    return self._lastLine

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

  def lines(self):
    return sorted(list(self._instructions.keys()))

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

      # There is no destination register for an output instruction,
      # as they don't write any values.
      if not isinstance(i, instructions.OutputInstruction):
        if i.rD() != None and i.rD() not in outputs:
          outputs.append(i.rD())

    if 0 in outputs:
      outputs.remove(0)

    # We've got all registers written to in this function,
    # now we need to see if we can do some pruning.

    # Step 1: returns
    # The MicroBlaze ABI defines the following register usage convention:
    # r0 - hardcoded 0
    # r1 - stack pointer
    # r2 - small data pointer, R
    # r3-r4 - volatile, return values/temp
    # r5-r10 - volatile, passing parameters/temp
    # r11-r12 - volatile, temp
    # r13 - small data pointer, RW
    # r14 - interrupt return address
    # r15 - subroutine return address
    # r16 - return address for trap
    # r17 - exception return address
    # r18 - assembler-reserved
    # r19-r31 - non-volatile, must be saved across function calls (callee save)

    # From this we can identify that:
    # r3-12 are caller save, and so will be restored upon returning from the function.
    # However, r3-r4 are function returns, so obviously are output registers from an end-of-function
    # block. Therefore, if the last instruction in this block is a return, we can exclude r5-r12.
    if self.last() != None and self.last().isReturn():
      for r in range(5, 13):
        if r in outputs:
          outputs.remove(r)

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
        currentBlock = BasicBlock("nolabel_line{:04d}".format(i), currentFunction, None)

      # If the instruction is a NOP and we're not already in the middle
      # of a basic block, ignore it and skip ahead.
      if type(s) is instructions.NOPInstruction and (len(currentBlock) == 0 or currentBlock == None):
        currentBlock = None
        continue

      if s.isBasicBlockBoundary():
        currentBlock.setLast(i, s)
        blocks.append(currentBlock)
        currentBlock = BasicBlock("nolabel_line{:04d}".format(i), currentFunction, None)
      else:
        currentBlock.add(i, s)
    elif s.isLabel():
      if currentBlock != None:
        blocks.append(currentBlock)

      if currentFunction == None:
        logger.warn("No function detected for label " + s.name() + ". Ignoring label.")
      else:
        currentBlock = BasicBlock(s.name() + "_line{:04d}".format(i), currentFunction, s.name())
    elif s.isDirective():
      if s.directive() == "type" and s.args(1) == "@function":
          currentFunction = s.args(0)

  if len(currentBlock) > 0:
    blocks.append(currentBlock)

  blocks = list(filter(lambda b: len(b) > 0, blocks))

  splitBlocks = []

  for block in blocks:
    split = False

    if block.last() != None:
      if block.last().isBranch():
        branchLabel = block.last().label()

        if branchLabel[0] == ".":
          offset = int(branchLabel[1:])//4
          line = block.lastLine() + offset

          splitBlocks += block.splitAtLine(line)
          logger.debug("Block " + block.name() + " split at line " + str(line) + ".")
          split = True

    if not split:
      splitBlocks.append(block)

  return linkBasicBlocks(logger, splitBlocks)

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
    if lastInstruction != None and not lastInstruction.isBasicBlockBoundary():
      raise ValueError("Expected control flow instruction as end of block " + b.name() + ", got " + str(lastInstruction))

    # If this is a normal branch instruction, find the block we're branching to.
    if lastInstruction != None:
      if lastInstruction.isBranch():
        branchLabel = lastInstruction.label()

        # If the label starts with '.', it's relative to the current location.
        if branchLabel[0] == ".":
          # Get the line specified by the relative label.
          offset = int(branchLabel[1:]) // 4
          line = b.lastLine() + offset

          foundBlock = None
          for otherB in blocks:
            startLine = otherB.lines()[0]
            if startLine == line:
              foundBlock = otherB

          if foundBlock == None:
            logger.warn("No target found for relative jump " + branchLabel + " in block " + b.name() + ".")
          else:
            logger.debug("Found next block for " + b.name() + ": " + foundBlock.name() + " from relative label " + branchLabel + ".")
            b.addNext(foundBlock)
        else:
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

        # Find all callsites for this function.
        callsites = []
        for otherB in blocks:
          if otherB.last() != None and otherB.last().label() == currentFunction:
            logger.debug("Found callsite for function " + currentFunction + " in block " + otherB.name())
            callsites.append(otherB)

        # For each callsite, identify the return instruction.
        # This is usually the next instruction (textually speaking),
        # but in the case of delayed-branch instructions, we actually skip ahead two instructions
        # (because the instruction immediately after the delayed-branch is the delay slot instruction).
        for otherB in callsites:
          # line number of last instruction
          lineNo = otherB.lastLine()

          if otherB.last() != None and otherB.last().hasDelay():
            returnLine = lineNo + 2
          else:
            returnLine = lineNo + 1

          # Find the next block at this line.
          foundBlock = None
          while foundBlock == None:
            for searchBlock in blocks:
              if searchBlock.lines()[0] == returnLine:
                foundBlock = searchBlock

            returnLine += 1

          logger.debug("Found return block for function " + currentFunction + ": block " + foundBlock.name())
          b.addNext(foundBlock)

        # We can't know if we've found all return sites for this function, so add an unknown next.
        b.addUnknownNext()

    # Otherwise this basic block simply runs into another one. Find the next block.
    else:
      nextLine = b.lines()[-1] + 1

      foundBlock = None
      while foundBlock == None:
        for otherB in blocks:
          startLine = otherB.lines()[0]
          if startLine == nextLine:
            foundBlock = otherB

        nextLine += 1

      logger.debug("Found next block for " + b.name() + ": " + foundBlock.name() + ".")
      b.addNext(foundBlock)

  return blocks
