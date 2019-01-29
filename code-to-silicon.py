from parsing import parser
from toolchain import compiler

compiler.compile(["c/main.c"], "main.s")

instructionList = [
  "add r1, r2, r3"
]

instructionListParsed = parser.parse(instructionList)

while instructionListParsed != None:
  print(instructionListParsed)
  instructionListParsed = instructionListParsed.getNext()