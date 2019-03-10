import math

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

    self._outputs = None

    self._inputs = []
    self._memoryAccessDensity = None
    self._averageComputationWidth = None
    self._cost = None

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

    if self._last != None:
      s += "\t{:04d}: {:s}\n".format(self._lastLine, str(self._last))

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

  def startLine(self):
    if len(self.lines()) > 0:
      return self.lines()[0]

    return self._lastLine

  def cost(self):
    if self._cost == None:
      raise ValueError("Cost not defined.")

    return self._cost

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
    if self._last == None:
      return self.lines()[-1]

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

  def getNext(self):
    return (self._next, self._unknownNext)

  def lines(self):
    return sorted(list(self._instructions.keys()))

  def memoryAccessDensity(self):
    if self._memoryAccessDensity == None:
      raise ValueError("Memory access density not defined.")

    return self._memoryAccessDensity

  def averageComputationWidth(self):
    if self._averageComputationWidth == None:
      raise ValueError("Average computation width not defined.")

    return self._averageComputationWidth

  def rawOutputs(self):
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

    return outputs

  def outputs(self):
    if self._outputs == None:
      raise ValueError("Block outputs not yet defined.")

    return self._outputs

  def setInputs(self):
    outputs = []

    for l in sorted(list(self._instructions.keys())):
      i = self._instructions[l]
      if i.rA() != None and i.rA() not in self._inputs and i.rA() not in outputs:
        self._inputs.append(i.rA())

      if i.rB() != None and i.rB() not in self._inputs and i.rB() not in outputs:
        self._inputs.append(i.rB())

      if isinstance(i, instructions.OutputInstruction):
        if i.rD() != None and i.rD() not in self._inputs:
          self._inputs.append(i.rD())
      else:
        if i.rD() != None and i.rD() not in outputs:
          outputs.append(i.rD())

    # r0 can be ignored as it is hardwired to 0.
    if 0 in self._inputs:
      self._inputs.remove(0)

  def setMemoryAccessDensity(self):
    numInstructions = 0
    numMemoryAccess = 0

    for l in self._instructions.keys():
      numInstructions += 1
      if self._instructions[l].isMemoryAccess():
        numMemoryAccess += 1

    if numInstructions == 0:
      self._memoryAccessDensity = 0
    else:
      self._memoryAccessDensity = (float(numMemoryAccess)/float(numInstructions))

  def setAverageComputationWidth(self):
    widths = []

    currentWidth = 0.0
    for l in sorted(list(self._instructions.keys())):
      if self._instructions[l].isMemoryAccess():
        widths.append(1.0)
        currentWidth = 0.0
      else:
        currentWidth += 1.0

    if currentWidth > 0.0:
      widths.append(currentWidth)

    if len(widths) == 0:
      self._averageComputationWidth = 0
    else:
      self._averageComputationWidth = (sum(widths)/len(widths))

  def setOutputs(self, logger, mode):
    self._outputs = self.rawOutputs()

    if mode == "naive":
      logger.debug("Pruning mode 'naive' completed for block " + self._name + ".")
      return

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
        if r in self._outputs:
          self._outputs.remove(r)

    if mode == "volatile":
      logger.debug("Pruning mode 'volatile' completed for block " + self._name + ".")
      return

    # If this block has a successor we do not know, stop, as there is no point trying to
    # see if we can prune any outputs. Note that we assume any unknown successor to take all registers
    # as inputs (this is the most pessimistic approach but also the only safe one).
    if self._unknownNext:
      logger.debug("Pruning mode 'dependency' completed for block " + self._name + ".")
      return

    # Now we can do some more expensive pruning. Consider:
    # A register is an output from a block B iff
    #   a. it is an input to some block B' which is a successor of B
    #   b. it is not the output of some block B* which is on the path between B and B'.
    #
    # First step: for each input, construct a set of lists that track it to its next input.
    for r in self._outputs:
      neededForBranch = False

      # Determine if this register is needed for a branch at the end of this block.
      if self._last != None:
        i = self._last
        if i.rA() != None and i.rA() == r:
          neededForBranch = True
        if i.rB() != None and i.rB() == r:
          neededForBranch = True

      if not neededForBranch:
        t = _track(self, r, [])

        t = sorted(t, key=lambda v: -len(v))

        removeRegister = True
        for visited in t:
          if not _isOutBeforeIn(r, visited[1:]):
            removeRegister = False
            break

        if removeRegister:
          self._outputs.remove(r)

    logger.debug("Pruning mode 'dependency' completed for block " + self._name + ".")

  def setCost(self):
    # We don't want to convert empty basic blocks, so their cost is effectively infinite.
    if len(self._instructions) == 0:
      self._cost = math.inf
    else:
      io_overhead = (len(self._outputs) + len(self._inputs))
      predicted_parallelism = self.averageComputationWidth()
      self._cost = io_overhead / predicted_parallelism

  def inputs(self):
    return self._inputs

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

    # r0 can be ignored as it is hardwired to 0.
    if 0 in used:
      used.remove(0)

    return used

# Given a block and a register, return all blocks which are direct successors which do not have
# that register as an input.
# In addition, return a flag if this block has a successor which is unknown to us (i.e. it is not a block we are analysing).
def _track(block, register, visited):
  # Stop if we've seen this block before, as this implies a loop.
  if block in visited:
    visited.append(block)
    return [visited]

  # Stop if this block has no successors.
  if len(block.getNext()[0]) == 0:
    visited.append(block)
    return [visited]

  # Stop if this block is at the end of a function and we're tracking a volatile register.
  if register in range(5, 13) and block.last() != None and block.last().isReturn():
    visited.append(block)
    return [visited]

  # Stop if the tracked register is an input to this block.
  if register in block.inputs():
    visited.append(block)
    return [visited]

  # We've now visited this block.
  visited.append(block)

  # For every block that is a successor of the current one:
  #
  # get all the lists returned by track() for that block.
  # Create a new list of lists.
  allVisited = []
  for b_next in block.getNext()[0]:
    l = _track(b_next, register, visited.copy())
    allVisited += l

  return allVisited

def _isOutBeforeIn(register, visited):
  output = False
  for block in visited:
    if block.getNext()[1] and not output:
      if register not in range(3, 5) and register not in range(11, 13):
        return False

    if output == False and register in block.inputs():
      return False

    if register in block.rawOutputs():
      output = True

  return True

def extractBasicBlocks(logger, stream, mode):
  blocks = []

  currentBlock = None
  currentFunction = None

  delaySlot = False
  delayBranch = None

  for i in range(len(stream)):
    s = stream[i]

    if delaySlot:
      if not s.isInstruction():
        raise ValueError("Expected instruction in delay slot, got " + str(s))

      logger.debug("Set delay slot for instruction " + str(currentBlock.last().mnemonic()) + ".")

      currentBlock.last().setDelay(s)
      delaySlot = False
      currentBlock =  None

    elif s.isInstruction():
      if currentBlock == None:
        currentBlock = BasicBlock("nolabel_line{:04d}".format(i), currentFunction, None)

      # If the instruction is a NOP and we're not already in the middle
      # of a basic block, ignore it and skip ahead.
      if type(s) is instructions.NOPInstruction and (len(currentBlock) == 0 or currentBlock == None):
        currentBlock = None

      elif s.isBasicBlockBoundary():
        currentBlock.setLast(i, s)
        blocks.append(currentBlock)

        if s.hasDelay():
          delaySlot = True
        else:
          currentBlock = None
      elif not delaySlot:
        currentBlock.add(i, s)
    elif s.isLabel():
      if currentBlock != None:
        blocks.append(currentBlock)

      if currentFunction == None:
        logger.warn("No function detected for label " + s.name() + ". Ignoring label.")
      else:
        escapedName = s.name().replace("$", "D_")
        currentBlock = BasicBlock(escapedName + "_line{:04d}".format(i), currentFunction, s.name())
    elif s.isDirective():
      if s.directive() == "type" and s.args(1) == "@function":
          currentFunction = s.args(0)

  if len(currentBlock) > 0:
    blocks.append(currentBlock)

  blocks = list(filter(lambda b: len(b) > 0 or b.last() != None, blocks))

  return linkBasicBlocks(logger, blocks, mode)

def linkBasicBlocks(logger, blocks, mode):
  for i in range(len(blocks)):
    # A basic block can be linked to another in one of two ways:
    # 1. a branch instruction
    # 2. a return
    #
    # We can always know the label to which we're jumping (as it's in the instruction itself),
    # but we might not always know where we're returning to (e.g. if the call site is in another compilation unit.)

    b = blocks[i]

    runOn = True
    lastInstruction = b.last()
    if lastInstruction != None and not lastInstruction.isBasicBlockBoundary():
      raise ValueError("Expected control flow instruction as end of block " + b.name() + ", got " + str(lastInstruction))

    # If this is a normal branch instruction, find the block we're branching to.
    if lastInstruction != None:
      if lastInstruction.isBranch():
        runOn = False

        branchLabel = lastInstruction.label()

        blocksWithLabel = list(filter(lambda b: b.label() == branchLabel, blocks))

        if len(blocksWithLabel) > 1:
          raise ValueError("Label " + branchLabel + " is ambiguous (" + str(len(blocksWithLabel)) + " matches)")
        elif len(blocksWithLabel) < 1:
          logger.warn("Unknown label: " + branchLabel)
          b.addUnknownNext()
        else:
          b.addNext(blocksWithLabel[0])

        # If the branch is conditional, we also need to link to the block after this one.]
        if lastInstruction.isConditional():
          runOn = True

      elif lastInstruction.isReturn():
        runOn = False

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
              if searchBlock.startLine() == returnLine:
                foundBlock = searchBlock

            returnLine += 1

          logger.debug("Found return block for function " + currentFunction + ": block " + foundBlock.name())
          b.addNext(foundBlock)

        # We can't know if we've found all return sites for this function, so add an unknown next.
        b.addUnknownNext()

    # This basic block simply runs into another one. Find the next block.
    if runOn:
      nextLine = b.lastLine() + 1

      foundBlock = None
      while foundBlock == None:
        for otherB in blocks:
          startLine = otherB.startLine()
          if startLine == nextLine:
            foundBlock = otherB

        nextLine += 1

      logger.debug("Found next block for " + b.name() + ": " + foundBlock.name() + ".")
      b.addNext(foundBlock)

  # Set inputs for ALL BLOCKS first, before doing anything else.
  for block in blocks:
    block.setInputs()

  # Set outputs for ALL BLOCKS.
  for block in blocks:
    block.setOutputs(logger, mode)

  # Set metrics and cost for ALL BLOCKS.
  for block in blocks:
    block.setMemoryAccessDensity()
    block.setAverageComputationWidth()
    block.setCost()

  return blocks
