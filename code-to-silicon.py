from parsing import parser
from toolchain import compiler

from analysis import basicblocks
from analysis import statemachine

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

selectedBlocks = list(filter(lambda b: b.memoryAccessDensity() <= 0.5, blocks))
selectedBlocks = list(filter(lambda b: (len(b.inputs()) + len(b.outputs())) < len(b), selectedBlocks))
selectedBlocks = list(filter(lambda b: len(b) > 1, selectedBlocks))

for block in selectedBlocks:
  print(block)

states = statemachine.getStateMachine(blocks[0])

compiler.assemble(["main.s"], "main.o")