import os

from parsing import parser
from toolchain import compiler, memory

from analysis import basicblocks
from analysis import statemachine

from translation import translator

instructions = [
    "10110000000000000100010010100000",
    "00100000001000000000000000000000",
    "00100000010000000000000000001111",
    "11111000010000010000000000000000"
]

words = list(map(lambda i: int(i, 2), instructions))

memory.writeMemoryFile("test.coe", words, 2048)

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

if len(memoryDensities) > 0:
  averageMemoryDensity = sum(memoryDensities) / len(memoryDensities)
else:
  averageMemoryDensity = 0

if len(inputSizes) > 0:
  averageInputSize = sum(inputSizes) / len(inputSizes)
else:
  averageInputSize = 0

if len(outputSizes) > 0:
  averageOutputSize = sum(outputSizes) / len(outputSizes)
else:
  averageOutputSize = 0

print("Mean memory density: " + str(round(averageMemoryDensity, 2)))
print("Mean input size: " + str(averageInputSize))
print("Mean output size: " + str(averageOutputSize))

selectedBlocks = list(filter(lambda b: b.memoryAccessDensity() <= 0.5, blocks))
selectedBlocks = list(filter(lambda b: (len(b.inputs()) + len(b.outputs())) < len(b), selectedBlocks))


#for block in selectedBlocks:
#  print(block)

sm = statemachine.getStateMachine(blocks[0])

with open(os.path.join("figures", "autogen", "statemachine.tex"), "w") as stream:
  stream.write(sm.toTikzDef())

with open("test.vhd", "w") as stream:
  stream.write(translator.translateStateMachine(sm))

compiler.link(["main.s", "start.s"], "main.elf")
compiler.makeHex("main.elf", "main.hex")
compiler.disassembleElf("main.elf", "main.asm")

# Now build the report!

os.system("pdflatex REPORT > texbuild.log")
os.system("biber REPORT > texbuild.log")
os.system("pdflatex REPORT > texbuild.log")

print("States: " + str(len(sm)))
