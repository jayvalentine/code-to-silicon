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

head = parser.parse(instructionList)

parser.prettyPrint(head)

#while instructionListParsed != None:
#  print(instructionListParsed)
#  instructionListParsed = instructionListParsed.getNext()