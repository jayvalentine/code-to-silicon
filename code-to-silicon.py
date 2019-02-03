from parsing import parser
from toolchain import compiler

import analysis

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

blocks = analysis.extractBlocks(instructionListParsed)

for block in blocks:
  r = analysis.analyseBlock(block)

  if r != None:
    for instruction in block:
      print(instruction)

    print("Inputs: ")
    print(r[0])
    print("Outputs: ")
    print(r[1])
    print("")

compiler.assemble(["main.s"], "main.o")