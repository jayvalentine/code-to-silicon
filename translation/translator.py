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
  s = ""

  s += getEntityDeclaration(stateMachine)

  s += "\n"

  s += getArchitecturalDefinition(stateMachine)

  return s

def getEntityDeclaration(stateMachine):
  tw = text.TextWriter(4)

  entityName = "hw_core_" + stateMachine.name()

  # Write library using statements.
  tw.writeLine("library IEEE;")
  tw.writeLine("use IEEE.STD_LOGIC_1164.ALL;")
  tw.writeLine("use IEEE.NUMERIC_STD.ALL;")

  tw.writeBlankLine()

  # Write the entity declaration.
  tw.writeLine("entity " + entityName + " is")

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
    tw.writeLine("in_" + "r{:02d}".format(r) + "      : in std_logic_vector(31 downto 0);")

  # Outputs for each register.
  tw.writeBlankLine()
  for r in stateMachine.outputRegisters():
    tw.writeLine("out_" + "r{:02d}".format(r) + "     : in std_logic_vector(31 downto 0);")

  # Done signal.
  tw.writeBlankLine()
  tw.writeLine("done        : out std_logic")

  tw.decreaseIndent()
  tw.writeLine(");")
  tw.decreaseIndent()
  tw.writeLine("end " + entityName + ";")

  return str(tw)

def getArchitecturalDefinition(stateMachine):
  tw = text.TextWriter(4)

  entityName = "hw_core_" + stateMachine.name()

  # Write architectural definition.
  tw.writeLine("architecture " + entityName + "_behav of " + entityName + "is")

  # Write type definition of STATE type.
  tw.increaseIndent()
  tw.writeLine("type STATE is (")
  tw.increaseIndent()
  tw.writeLine("S_RESET,")

  for i in range(len(stateMachine)-1):
    tw.writeLine(stateMachine[i].name() + ",")

  tw.writeLine(stateMachine[len(stateMachine)-1].name())
  tw.decreaseIndent()
  tw.writeLine(");")

  tw.writeBlankLine()

  # Declaration of internal state register.
  tw.writeLine("signal int_state    : STATE;")
  tw.writeBlankLine()

  # Declaration of internal registers.
  for r in stateMachine.usedRegisters():
    tw.writeLine("signal " + "r{:02d}".format(r) + "          :signed(31 downto 0);")

  # Begin behavioural definition.
  tw.decreaseIndent()
  tw.writeBlankLine()
  tw.writeLine("begin")

  # Begin process.
  tw.increaseIndent()
  tw.writeLine("process(clk, m_rdy, rst")
  tw.increaseIndent()

  # Output local variables for each state.
  # These are 'namespaced' by state name so they don't conflict.
  for i in range(len(stateMachine)):
    for local in stateMachine[i].locals():
      tw.writeLine("variable " + stateMachine[i].name() + "_r{:02d}".format(local) + "   : signed(31 downto 0);")
    
    if len(stateMachine[i].locals()) > 0:
      tw.writeBlankLine()

  # Start the process body.
  tw.decreaseIndent()
  tw.writeLine("begin")
  tw.increaseIndent()

  # Reset condition. If rst = 1 then reset internal values.
  tw.writeLine("if rst = '1' then")
  tw.increaseIndent()
  tw.writeLine("int_state <= S_STATE;")
  tw.writeLine("m_data    <= (others => '0');")
  tw.writeLine("m_addr    <= (others => '0');")
  tw.writeLine("m_rd      <= '0';")
  tw.writeLine("m_wr      <= '0';")
  tw.writeLine("done      <= '0';")
  tw.decreaseIndent()

  # Rising clock edge condition.
  # If we're in a memory state, set the address and correct strobe.
  # If we're in a computation state, do some computation.
  # If we're in a start state, get some inputs.
  # If we're in an end state, write some outputs.
  # If we're in the reset state, move to the first state.
  tw.writeLine("elsif rising_edge(clk) then")
  tw.increaseIndent()

  # Reset state condition.
  tw.writeLine("if int_state = S_RESET then")
  tw.increaseIndent()
  tw.writeLine("int_state <= " + stateMachine[0].name() + ";")
  tw.decreaseIndent()

  # Other states.
  for i in range(len(stateMachine)):
    s = stateMachine[i]

    tw.writeBlankLine()
    tw.writeLine("elsif int_state = " + s.name() + " then")
    tw.increaseIndent()

    # If this is a start state, get inputs into the state machine's internal registers.
    if s.isStartState():
      for r in stateMachine.inputRegisters():
        tw.writeLine("r{reg:02d} <= in_r{reg:02d};".format(reg=r))

    # If this is an end state, put outputs from the state machine's internal registers.
    # Also set the done flag.
    elif s.isEndState():
      for r in stateMachine.outputRegisters():
        tw.writeLine("out_r{reg:02d} <= r{reg:02d};".format(reg=r))
      tw.writeLine("done <= '1';")

    # If this is a wait state, set up the memory transaction (either a read or a write).
    elif s.isWaitState():
      inst = s.instruction()
      # Figure out what the expression is for the memory address.
      # It's either rA+imm or rA+rB.
      if inst.imm != None:
        expr = "r{reg:02d} + {imm:d}".format(reg = inst.rA(), imm = inst.imm())
      else:
        expr = "r{regA:02d} + r{regB:02d}".format(regA = inst.rA(), regB = inst.rB())

      tw.writeLine("m_addr <= std_logic_vector(unsigned(" + expr + "));")

      # If the instruction is a read, we need to set the read strobe high.
      # If the instruction is a write, we need to set the write strobe high.
      if inst.isRead():
        tw.writeLine("m_rd <= '1';")
      else:
        tw.writeLine("m_wr <= '1';")


    # We transition to the next state if this is not a wait state.
    if "CLK" in s.triggers() and s.getTransition("CLK") != s:
      tw.writeLine("int_state <= " + s.getTransition("CLK").name() + ";")
    
    tw.decreaseIndent()

  tw.writeLine("end " + entityName + "_behav;")

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