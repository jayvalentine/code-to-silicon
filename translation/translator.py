from . import text



ADD_FORMAT = "r{0:d} := r{1:d} + r{2:d}"
ADDI_FORMAT = "r{0:d} := r{1:d} + {2:d}"

MUL_FORMAT = "r{0:d} := r{1:d} * r{2:d}"
IDIV_FORMAT = "r{0:d} := r{1:d} / r{2:d}"
SRA_FORMAT = "r{0:d} := shift_right(r{1:d}, 1)"

MEM_ADDRESS_SET_IMM_FORMAT = "MEM_ADDR <= r{0:d} + {1:d}"
MEM_DATA_READ = "r{0:d} <= MEM_DATA_IN"
MEM_DATA_WRITE = "MEM_DATA_OUT <= r{0:d}"

def translateStateMachine(stateMachine):
  return getEntityDeclaration(stateMachine)

def getEntityDeclaration(stateMachine):
  tw = text.TextWriter(4)

  # Write library using statements.
  tw.writeLine("library IEEE;")
  tw.writeLine("use IEEE.STD_LOGIC_1164.ALL;")
  tw.writeLine("use IEEE.NUMERIC_STD.ALL;")

  tw.writeBlankLine()

  # Write the entity declaration.
  tw.writeLine("entity hw_core_" + stateMachine.name() + " is")

  # Write port definitions.
  tw.increaseIndent()
  tw.writeLine("port (")
  tw.increaseIndent()

  # CLK, M_RDY, and RST signals.
  tw.writeLine("clk         : in std_logic;")
  tw.writeLine("rst         : in std_logic;")
  tw.writeLine("m_rdy       : in std_logic;")

  # Read and write strobes.
  tw.writeBlankLine()
  tw.writeLine("m_wr        : out std_logic;")
  tw.writeLine("m_rd        : out std_logic;")

  # Memory address and data lines.
  tw.writeBlankLine()
  tw.writeLine("m_addr      : out std_logic_vector(31 downto 0);")
  tw.writeLine("m_data      : inout std_logic_vector(31 downto 0);")

  # Inputs for each register.
  tw.writeBlankLine()
  for r in stateMachine.inputRegisters():
    tw.writeLine("in_" + "{:02d}".format(r) + "      : in std_logic_vector(31 downto 0);")

  # Outputs for each register.
  tw.writeBlankLine()
  for r in stateMachine.outputRegisters():
    tw.writeLine("out_" + "{:02d}".format(r) + "     : in std_logic_vector(31 downto 0);")

  # Done signal.
  tw.writeBlankLine()
  tw.writeLine("done        : out std_logic")

  tw.decreaseIndent()
  tw.writeLine(");")
  tw.decreaseIndent()
  tw.writeLine("end hw_core_" + stateMachine.name() + ";")

  return str(tw)

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