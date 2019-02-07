ADD_FORMAT = "r{0:d} := r{1:d} + r{2:d}"
ADDI_FORMAT = "r{0:d} := r{1:d} + {2:d}"

MUL_FORMAT = "r{0:d} := r{1:d} * r{2:d}"
IDIV_FORMAT = "r{0:d} := r{1:d} / r{2:d}"
SRA_FORMAT = "r{0:d} := shift_right(r{1:d}, 1)"

MEM_ADDRESS_SET_IMM_FORMAT = "MEM_ADDR <= r{0:d} + {1:d}"
MEM_DATA_READ = "r{0:d} <= MEM_DATA_IN"
MEM_DATA_WRITE = "MEM_DATA_OUT <= r{0:d}"

def translateMemoryAccess(instruction):
  mnemonic = instruction.mnemonic()

  if mnemonic == "swi":
    s = MEM_ADDRESS_SET_IMM_FORMAT.format(instruction.rA(), instruction.imm()) + "\n"
    s += MEM_DATA_WRITE.format(instruction.rD())
    return s
  elif mnemonic == "lwi":
    s = MEM_ADDRESS_SET_IMM_FORMAT.format(instruction.rA(), instruction.imm()) + "\n"
    s += MEM_DATA_READ.format(instruction.rD())
    return s
  else:
    raise ValueError("Unknown instruction for translation: " + str(instruction))

# Translates a given instruction into one or more lines of VHDL.
def translateArithmetic(instruction):
  mnemonic = instruction.mnemonic()

  if mnemonic == "addk":
    return ADD_FORMAT.format(instruction.rD(), instruction.rA(), instruction.rB())
  elif mnemonic == "addik":
    return ADDI_FORMAT.format(instruction.rD(), instruction.rA(), instruction.imm())
  elif mnemonic == "mul":
    return MUL_FORMAT.format(instruction.rD(), instruction.rA(), instruction.rB())
  elif mnemonic == "idiv":
    return IDIV_FORMAT.format(instruction.rD(), instruction.rA(), instruction.rB())
  elif mnemonic == "sra":
    return SRA_FORMAT.format(instruction.rD(), instruction.rA())
  else:
    raise ValueError("Unknown instruction for translation: " + str(instruction))