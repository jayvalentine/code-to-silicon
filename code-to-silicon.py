from parsing import parser
from toolchain import compiler

from analysis import basicblocks
from analysis import statemachine

from translation import translator

compiler.compile(["c/main.c"], "main.s")

with open("main.s", 'r') as stream:
  instructionList = stream.readlines()

  # Filter out blank lines
  instructionList = list(filter(lambda l: len(l.lstrip()) > 0, instructionList))

  # Filter out directives, which begin with '.'
  instructionList = list(filter(lambda l: l.lstrip()[0] != '.', instructionList))

  # Filter out comment lines (but NOT instructions with comments on the end)
  instructionList = list(filter(lambda l: l.lstrip()[0] != '#', instructionList))

#print(instructionList)

instructionListParsed = parser.parse(instructionList)

#parser.prettyPrint(head)

blocks = basicblocks.extractBasicBlocks(instructionListParsed)

# Filter blocks with a length of 1. We don't really care about them so we don't
# want to include them in the analysis.
blocks = list(filter(lambda b: len(b) > 1, blocks))

# Get some statistics about the blocks.
memoryDensities = []
inputSizes = []
outputSizes = []

for block in blocks:
  memoryDensities.append(block.memoryAccessDensity())
  inputSizes.append(len(block.inputs()))
  outputSizes.append(len(block.outputs()))

averageMemoryDensity = sum(memoryDensities) / len(memoryDensities)
averageInputSize = sum(inputSizes) / len(inputSizes)
averageOutputSize = sum(outputSizes) / len(outputSizes)

print("Mean memory density: " + str(round(averageMemoryDensity, 2)))
print("Mean input size: " + str(averageInputSize))
print("Mean output size: " + str(averageOutputSize))

selectedBlocks = list(filter(lambda b: b.memoryAccessDensity() <= 0.5, blocks))
selectedBlocks = list(filter(lambda b: (len(b.inputs()) + len(b.outputs())) < len(b), selectedBlocks))


#for block in selectedBlocks:
#  print(block)

states = statemachine.getStateMachine(blocks[0])

for state in states:
  if state.isWaitState():
    print("Wait:")
    print(translator.translateMemoryAccess(state.instruction()))
  elif state.isStartState():
    print("Start:")
  elif state.isEndState():
    print("End:")
  else:
    print("Computation:")
    for i in state.instructions():
      print(translator.translateArithmetic(i))

compiler.assemble(["main.s"], "main.o")