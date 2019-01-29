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
  def __init__(self, mnemonic, rA, rB, rD, imm):
    self._mnemonic = mnemonic
    self._rA = rA
    self._rB = rB
    self._rD = rD
    self._imm = imm

  """
  Returns string representation of instruction.
  """
  def __str__(self):
    s = ""
    s += self._mnemonic
    s += " "
    s += "r" + str(self._rD)
    s += ", "
    s += "r" + str(self._rA)
    s += ", "

    # If imm is None, we assume this is format A (2 source registers).
    # The last element of the string in this case is rB.
    # Otherwise it is the immediate as a hex string.
    if self._imm == None:
      s += "r" + str(self._rB)
    else:
      s += "0x{:04x}".format(self._imm)

    return s

  """
  Returns true if this instruction can be translated to VHDL, false otherwise.
  """
  def canTranslate():
    raise NotImplementedError("Abstract method. Must be overriden by subclasses.")

  """
  Returns true if this instruction forms the boundary of a basic block, false otherwise.
  """
  def isBasicBlockBoundary():
    raise NotImplementedError("Abstract method. Must be overriden by subclasses.")

  """
  Returns true if this instruction is a memory access, false otherwise.
  """
  def isMemoryAccess():
    raise NotImplementedError("Abstract method. Must be overriden by subclasses.")

"""
Base arithmetic/logic instructions. Both integer and float arithmetic/logic
instructions inherit from this.
"""
class ArithmeticInstruction(Instruction):
  def isBasicBlockBoundary():
    return False

  def isMemoryAccess():
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
  def canTranslate():
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
  def canTranslate():
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
  def canTranslate():
    return False

  def isBasicBlockBoundary():
    return True

  def isMemoryAccess():
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
  def canTranslate():
    return True

  def isBasicBlockBoundary():
    return False

  def isMemoryAccess():
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
  def canTranslate():
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
  def canTranslate():
    return True

  def isBasicBlockBoundary():
    return False

  def isMemoryAccess():
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
  def canTranslate():
    return False

  def isBasicBlockBoundary():
    return False

  def isMemoryAccess():
    return False