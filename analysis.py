def extractBlocks(stream):
  blocks = []

  currentBlock = []

  for s in stream:
    if s.isInstruction():
      if s.isBasicBlockBoundary():
        blocks.append(currentBlock)
        currentBlock = []
        currentBlock.append(s)
        blocks.append(currentBlock)
        currentBlock = []
      else:
        currentBlock.append(s)
    else:
      blocks.append(currentBlock)
      currentBlock = []
      currentBlock.append(s)
      blocks.append(currentBlock)
      currentBlock = []

  blocks.append(currentBlock)

  blocks = list(filter(lambda b: len(b) > 0, blocks))

  return blocks

def analyseBlock(block):
  if (not block[0].isInstruction()) or (block[0].isBasicBlockBoundary()):
    return None

  outputs = set()
  inputs = set()

  for instruction in block:
    if instruction.rA() != None and instruction.rA() not in outputs:
      inputs.add(instruction.rA())

    if instruction.rB() != None and instruction.rB() not in outputs:
      inputs.add(instruction.rB())

    if instruction.rD() != None:
      outputs.add(instruction.rD())

  # Ignore r0. r0 is always equal to 0 and anything written to r0 is discarded,
  # therefore it can't be an input (because it's a constant value) and it can't
  # be an output (because writes are discarded).
  if 0 in outputs:
    outputs.remove(0)
  if 0 in inputs:
    inputs.remove(0)

  return (inputs, outputs)