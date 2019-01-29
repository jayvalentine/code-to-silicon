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
  def __init__(self, mnemonic, rA, rB, rD, imm):
    self._mnemonic = mnemonic
    self._rA = rA
    self._rB = rB
    self._rD = rD
    self._imm = imm

  def __str__(self):
    s = ""
    s += self._mnemonic
    s += " "
    s += "r" + str(self._rD)
    s += ", "
    s += "r" + str(self._rA)
    s += ", "

    # If imm is None, we assume this is format A (2 source registers).
    if self._imm == None:
      s += "r" + str(self._rB)
    else:
      s += "0x{:04x}".format(self._imm)

    return s

