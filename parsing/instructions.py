import yaml
import os
import re

INSTRUCTION_MAPPING = {}

CONFIG_FILENAME = os.path.join(os.path.dirname(__file__), "instructions.yaml")

REGISTER_FORMAT_RE = re.compile("r(\d{1,2})")
IMMEDIATE_FORMAT_RE = re.compile("(-?\d+)")
LABEL_FORMAT_RE = re.compile("(\$\w)")

# We need to catagorise instructions. We do this in a YAML file
# that we then read in and convert into a dictionary mapping instruction
# mnemonics to categories.
with open(CONFIG_FILENAME, 'r') as stream:
  y = yaml.load(stream)

  for category in y.keys():
    mnemonics = y[category]

    for m in mnemonics:
      INSTRUCTION_MAPPING[m] = category

"""
Base instruction class. Actual instructions shouldn't use this directly,
but should instead inherit from this to create a custom subclass.

Attributes:
  - mnemonic  - instruction mnemonic (e.g. add, xori)
  - rA        - source register A
  - rB        - source register B (if applicable)
  - rD        - destination register
  - imm       - immediate value (if applicable)
"""
class Instruction:
  """
  Constructor.

  Parameters:
    - mnemonic - string mnemonic for instruction.
    - rA - number of source register A
    - rB - number of source register B
    - rD - number of destination register
    - imm - immediate value. None if no immediate.
  """
  def __init__(self, mnemonic, rA, rB, rD, imm, label):
    self._mnemonic = mnemonic
    self._rA = rA
    self._rB = rB
    self._rD = rD
    self._imm = imm
    self._label = label

    self._next = None

  """
  Returns string representation of instruction.
  """
  def __str__(self):
    tabCount = 1

    s = ""
    s += self._mnemonic
    s += "\t"

    if self._rD != None:
      s += "r" + str(self._rD)
      s += ", "
    else:
      tabCount = 2

    if self._rA != None:
      s += "r" + str(self._rA)
      s += ", "

    # If imm is None, we assume this is format A (2 source registers).
    # The last element of the string in this case is rB.
    # Otherwise it is the immediate or label.
    if self._imm == None and self._rB != None:
      s += "r" + str(self._rB)
    elif self._imm != None:
      s += str(self._imm)
    elif self._label != None:
      s += str(self._label)

    # Now append some flags for the metadata (is translatable, is memory access, etc)
    s += "\t" * tabCount

    if self.canTranslate():
      s += "T"
    else:
      s += "-"

    if self.isBasicBlockBoundary():
      s += "B"
    else:
      s += "-"

    if self.isMemoryAccess():
      s += "M"
    else:
      s += "-"

    return s

  """
  Sets next instruction. This is the next instruction in a textual sense,
  not in the sense of control flow (i.e. the next instruction on from a jump
  is 1 word after it in memory, not the jump target).
  """
  def setNext(self, instruction):
    self._next = instruction

  """
  Gets the next instruction. See setNext for an explanation of what this means.
  """
  def getNext(self):
    return self._next

  """
  Returns true if this instruction can be translated to VHDL, false otherwise.
  """
  def canTranslate(self):
    raise NotImplementedError("Abstract method. Must be overriden by subclasses.")

  """
  Returns true if this instruction forms the boundary of a basic block, false otherwise.
  """
  def isBasicBlockBoundary(self):
    raise NotImplementedError("Abstract method. Must be overriden by subclasses.")

  """
  Returns true if this instruction is a memory access, false otherwise.
  """
  def isMemoryAccess(self):
    raise NotImplementedError("Abstract method. Must be overriden by subclasses.")

"""
Base arithmetic/logic instructions. Both integer and float arithmetic/logic
instructions inherit from this.
"""
class ArithmeticInstruction(Instruction):
  def isBasicBlockBoundary(self):
    return False

  def isMemoryAccess(self):
    return False

"""
Integer arithmetic instructions. These are:

add
addi
rsub
rsubi
idiv
mul
mulh
mulhu
mulhsu
muli
and
andi
andn
andni
or
ori
xor
xori
bs
bsi
sra
src
srl
cmp
sext16
sext8
pcmpbf
pcmpeq
pcmpne
"""
class IntegerArithmeticInstruction(ArithmeticInstruction):
  def canTranslate(self):
    return True

"""
Floating-point arithmetic/logic instructions. These are:

fadd
frsub
fmul
fdiv
fcmp
flt
fint
fsqrt
"""
class FloatArithmeticInstruction(ArithmeticInstruction):
  def canTranslate(self):
    return False

"""
Control flow (branch/jump) instructions. These are:

beq
beqi
bge
bgei
bgt
bgti
ble
blei
blt
blti
bne
bnei
br
bri
brk
brki
rtbd
rtid
rted
rtsd
"""
class ControlFlowInstruction(Instruction):
  def __init__(self, mnemonic, rA, rB, rD, imm, label):
    # For a control flow instruction, there is no rD, so what is passed as rD becomes rA, and rA becomes
    # rB.
    super(ControlFlowInstruction, self).__init__(mnemonic, rD, rA, None, imm, label)

  def canTranslate(self):
    return False

  def isBasicBlockBoundary(self):
    return True

  def isMemoryAccess(self):
    return False

"""
Input/output instructions. These do not include the FSL-access instructions
as these are their own subclass. These are:

lbu
lbui
lhu
lhui
lw
lwi
sb
sbi
sh
shi
sw
swi
"""
class InputOutputInstruction(Instruction):
  def canTranslate(self):
    return True

  def isBasicBlockBoundary(self):
    return False

  def isMemoryAccess(self):
    return True

"""
FSL-access instructions. These are used for accessing Microblaze's FSL bus and so
are not translatable into hardware, nor do they form memory-access transitions for
accelerator state machines. These are:

get
getd
put
putd
"""
class FSLInputOutputInstruction(InputOutputInstruction):
  def canTranslate(self):
    return False

"""
Not really an instruction as such but is instead a way for an immediate (format B)
instruction to use a 32-bit immediate value rather than the standard 16-bit value.
If such an instruction is preceded immediately by an imm instruction, the imm instruction
value is 'locked' and is used by the next instruction.

There is only one such instruction:
imm
"""
class ImmediateInstruction(Instruction):
  def canTranslate(self):
    return True

  def isBasicBlockBoundary(self):
    return False

  def isMemoryAccess(self):
    return False

"""
These are instructions relating to system operation, and are therefore not translatable
as they make no sense outside of the context of executing on the Microblaze core.
These are:

mfs
mts
msrclr
msrset
"""
class SystemInstruction(Instruction):
  def canTranslate(self):
    return False

  def isBasicBlockBoundary(self):
    return False

  def isMemoryAccess(self):
    return False

"""
These are nop instructions. They are not translatable as there isn't really any point.
They will probably only occur in the case of unused delay slots in rtxd instructions.

nop
"""
class NOPInstruction(Instruction):
  def canTranslate(self):
    return False

  def isBasicBlockBoundary(self):
    return False

  def isMemoryAccess(self):
    return False

def parseInstruction(instructionString):
  # Sanitise the input slightly. We don't care about comments.
  # These begin with a '#' and start after the end of the instruction.
  if '#' in instructionString:
    instructionString = instructionString[:instructionString.index('#')]

  # Strip any leading and trailing whitespace.
  instructionString = instructionString.strip()

  originalInstructionString = instructionString

  if ' ' in instructionString or '\t' in instructionString:
    # First get the mnemonic. This is the first token in the string and
    # ends with the first space.
    try:
      mnemonic = instructionString[:instructionString.index(' ')]
    except ValueError:
      # Maybe its a tab?
      try:
        mnemonic = instructionString[:instructionString.index('\t')]
      except ValueError:
        raise ValueError("Error parsing mnemonic from instruction: " + originalInstructionString)
  else:
    mnemonic = instructionString

  # Find the category of the instruction and get the relevant class.
  try:
    category = INSTRUCTION_MAPPING[mnemonic]
  except KeyError:
    raise ValueError("Unknown mnemonic: " + mnemonic + " in instruction: " + originalInstructionString)

  if category == "IntegerArith":
    instructionClass = IntegerArithmeticInstruction
  elif category == "FloatArith":
    instructionClass = FloatArithmeticInstruction
  elif category == "ControlFlow":
    instructionClass = ControlFlowInstruction
  elif category == "InputOutput":
    instructionClass = InputOutputInstruction
  elif category == "FSL":
    instructionClass = FSLInputOutputInstruction
  elif category == "Immediate":
    instructionClass = ImmediateInstruction
  elif category == "System":
    instructionClass = SystemInstruction
  elif category == "NOP":
    instructionClass = NOPInstruction
  else:
    raise ValueError("Invalid category: " + str(category))

  # If there are no delimiters now, just return a blank instruction.
  if ' ' not in instructionString and '\t' not in instructionString:
    return instructionClass(mnemonic, None, None, None, None, None)

  # Now we have one or more whitespaces.
  try:
    instructionString = instructionString[instructionString.index(' '):]
  except ValueError:
    try:
      instructionString = instructionString[instructionString.index('\t'):]
    except ValueError:
      raise ValueError("Unknown delimiter in instruction: " + originalInstructionString)

  instructionString = instructionString.strip()

  instructionParameters = instructionString.split(',')
  instructionParameters = list(map(lambda p: p.strip(), instructionParameters))

  # Initialise all the parameters.
  sourceRegisterA = None
  sourceRegisterB = None
  destinationRegister = None
  immediate = None
  label = None

  if len(instructionParameters) < 1:
    return instructionClass(mnemonic, sourceRegisterA, sourceRegisterB, destinationRegister, immediate, label)

  # The first parameter is the destination register or a label.
  destinationRegister = parseRegister(instructionParameters[0])
  if destinationRegister == None:
    label = parseLabel(instructionParameters[0])
    if label == None:
      raise ValueError("Error parsing first parameter in instruction: " + originalInstructionString)

  if len(instructionParameters) < 2:
    return instructionClass(mnemonic, sourceRegisterA, sourceRegisterB, destinationRegister, immediate, label)

  # The second parameter is source register A, an immediate, or a label.
  sourceRegisterA = parseRegister(instructionParameters[1])
  if sourceRegisterA == None:
    immediate = parseImmediate(instructionParameters[1])
    if immediate == None:
      label = parseLabel(instructionParameters[1])
      if label == None:
        raise ValueError("Error parsing second parameter in instruction: " + originalInstructionString)

  if len(instructionParameters) < 3:
    return instructionClass(mnemonic, sourceRegisterA, sourceRegisterB, destinationRegister, immediate, label)

  sourceRegisterB = parseRegister(instructionParameters[2])
  if sourceRegisterB == None:
    immediate = parseImmediate(instructionParameters[2])
    if immediate == None:
      raise ValueError("Error parsing third parameter in instruction: " + originalInstructionString)

  return instructionClass(mnemonic, sourceRegisterA, sourceRegisterB, destinationRegister, immediate, label)

def parseRegister(s):
  m = REGISTER_FORMAT_RE.match(s)

  if m == None:
    return None

  return int(m.groups()[0])

def parseImmediate(s):
  m = IMMEDIATE_FORMAT_RE.match(s)

  if m == None:
    return None

  return int(m.groups()[0])

def parseLabel(s):
  m = LABEL_FORMAT_RE.match(s)

  if m == None:
    return None

  return str(m.groups()[0])