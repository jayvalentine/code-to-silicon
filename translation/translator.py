import text

ADD_FORMAT = "{:s} := {:s} + {:s};"
ADDI_FORMAT = "{:s} := {:s} + to_signed({:s}, 32);"

AND_FORMAT = "{:s} := {:s} and {:s};"
ANDI_FORMAT = "{:s} := {:s} and to_signed({:s}, 32);"

OR_FORMAT = "{:s} := {:s} or {:s};"
ORI_FORMAT = "{:s} := {:s} or to_signed({:s}, 32);"

XOR_FORMAT = "{:s} := {:s} xor {:s};"
XORI_FORMAT = "{:s} := {:s} xor to_signed({:s}, 32);"

SRL_FORMAT = "{:s} := {:s} srl 1;"

MUL_FORMAT = "{:s} := {:s} * {:s};"
MULI_FORMAT = "{:s} := {:s} * to_signed({:s}, 32);"

def translateStateMachine(stateMachine):
  s = ""

  s += getEntityDeclaration(stateMachine)

  s += "\n"

  s += getArchitecturalDefinition(stateMachine)

  return s

def getEntityDeclaration(stateMachine):
  tw = text.TextWriter(4, "--")

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

  ports = getPorts(stateMachine)
  for port in ports[:-1]:
    tw.writeLine(port[0] + " : " + port[1] + " " + port[2] + ";")

  tw.writeLine(ports[-1][0] + " : " + ports[-1][1] + " " + ports[-1][2])

  tw.decreaseIndent()
  tw.writeLine(");")
  tw.decreaseIndent()
  tw.writeLine("end " + entityName + ";")

  return str(tw)

def getArchitecturalDefinition(stateMachine):
  tw = text.TextWriter(4, "--")

  entityName = "hw_core_" + stateMachine.name()

  # Write architectural definition.
  tw.writeLine("architecture " + entityName + "_behav of " + entityName + " is")

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
    if r != 0:
      tw.writeLine("signal " + "r{:02d}".format(r) + "          : signed(31 downto 0);")

  # Constant r0, which is a hardwired 0 value.
  tw.writeLine("constant r00          : signed(31 downto 0) := x\"00000000\";")

  # Output the 'offset' signal. This is used for calculating offsets for IO of bytes and halfwords.
  tw.writeCommentLine("Offset.")
  tw.writeLine("signal offset         :  Integer;")
  tw.writeBlankLine()

  # Begin behavioural definition.
  tw.decreaseIndent()
  tw.writeBlankLine()
  tw.writeLine("begin")

  # Begin process.
  tw.increaseIndent()
  tw.writeLine("process(clk, m_rdy, rst)")
  tw.increaseIndent()

  # Output local variables for each state.
  # These are 'namespaced' by state name so they don't conflict.
  for i in range(len(stateMachine)):
    if len(stateMachine[i].locals()) > 0:
      tw.writeCommentLine("State "
                          + stateMachine[i].name()
                          + " Locals: "
                          + ", ".join(list(map(lambda r: "r{:02d}".format(r), stateMachine[i].locals())))
                          + ".")

    for local in stateMachine[i].locals():
      if local != 0:
        tw.writeLine("variable " + localName(stateMachine[i].name(), local) + "   : signed(31 downto 0);")

    if len(stateMachine[i].locals()) > 0:
      tw.writeBlankLine()

  # Output the 'temp64' variable. This is used by operations which produce a 64-bit result (e.g. multiply)
  tw.writeCommentLine("Temporary 64-bit variable.")
  tw.writeLine("variable temp64      : signed(63 downto 0);")
  tw.writeBlankLine()

  # Start the process body.
  tw.decreaseIndent()
  tw.writeLine("begin")
  tw.increaseIndent()

  # Reset condition. If rst = 1 then reset internal values.
  tw.writeLine("if rst = '1' then")
  tw.increaseIndent()
  tw.writeLine("int_state  <= S_RESET;")
  tw.writeLine("m_data_out <= (others => '0');")
  tw.writeLine("m_addr     <= (others => '0');")

  tw.writeBlankLine()

  for out in stateMachine.outputRegisters():
    tw.writeLine("out_r{:02d} <= (others => '0');".format(out))

  tw.writeBlankLine()

  tw.writeLine("m_rd       <= '0';")
  tw.writeLine("m_wr       <= \"0000\";")
  tw.writeLine("done       <= '0';")

  tw.decreaseIndent()

  tw.writeLine("elsif sel = '1' then")

  tw.increaseIndent()

  # Rising clock edge condition.
  # If we're in a memory state, set the address and correct strobe.
  # If we're in a computation state, do some computation.
  # If we're in a start state, get some inputs.
  # If we're in an end state, write some outputs.
  # If we're in the reset state, move to the first state.
  tw.writeLine("if rising_edge(clk) then")
  tw.increaseIndent()

  tw.writeLine("case int_state is")

  # Reset state condition.
  tw.writeLine("when S_RESET =>")
  tw.increaseIndent()
  tw.writeLine("int_state <= " + stateMachine[0].name() + ";")
  tw.decreaseIndent()

  # Other states.
  for i in range(len(stateMachine)):
    s = stateMachine[i]

    tw.writeBlankLine()
    tw.writeLine("when " + s.name() + " =>")
    tw.increaseIndent()

    # If this is a start state, get inputs into the state machine's internal registers.
    if s.isStartState():
      for r in stateMachine.inputRegisters():
        tw.writeLine("r{reg:02d} <= signed(in_r{reg:02d});".format(reg=r))
      tw.writeBlankLine()

    # If this is an end state, put outputs from the state machine's internal registers.
    # Also set the done flag.
    elif s.isEndState():
      for r in stateMachine.outputRegisters():
        tw.writeLine("out_r{reg:02d} <= std_logic_vector(r{reg:02d});".format(reg=r))
      tw.writeLine("done <= '1';")
      tw.writeBlankLine()

    # If this is a wait state, set up the memory transaction (either a read or a write).
    elif s.isWaitState():
      inst = s.instruction()
      # Figure out what the expression is for the memory address.
      # It's either rA+imm or rA+rB.
      if inst.imm() != None:
        expr = "(r{reg:02d} + to_signed({imm:d}, 32))".format(reg = inst.rA(), imm = inst.imm())
      elif inst.label() != None:
        expr = "(r{reg:02d} + to_signed({imm:s}, 32))".format(reg = inst.rA(), imm = "%%SYM_" + inst.label() + "%%")
      else:
        expr = "(r{regA:02d} + r{regB:02d})".format(regA = inst.rA(), regB = inst.rB())

      tw.writeCommentLine(str(inst))
      tw.writeLine("m_addr <= std_logic_vector(unsigned(" + expr + "));")

      # If the instruction is a read, we need to set the read strobe high.
      # If the instruction is a write, we need to set the write strobe high AND set the data out line.
      if inst.width() == 1:
        tw.writeLine("offset <= (to_integer(" + expr + ") mod 4) * 8;")
      elif inst.width() == 2:
        tw.writeLine("offset <= (to_integer(" + expr + ") mod 4) * 16;")

      if inst.isRead():
        tw.writeLine("m_rd <= '1';")
      else:
        if inst.width() == 1:
          tw.writeLine("m_data_out <= (others => '0');")
          tw.writeLine("m_data_out((offset+7) downto offset) <= std_logic_vector(unsigned(r{:02d}))(7 downto 0);".format(inst.rD()))
        elif inst.width() == 2:
          tw.writeLine("m_data_out <= (others => '0');")
          tw.writeLine("m_data_out((offset+15) downto offset) <= std_logic_vector(unsigned(r{:02d}))(15 downto 0);".format(inst.rD()))
        elif inst.width() == 4:
          tw.writeLine("m_data_out <= std_logic_vector(unsigned(r{:02d}));".format(inst.rD()))

        # Set up the write enable.
        tw.writeLine("m_wr <= \"0000\";")
        if inst.width() == 1:
          tw.writeLine("m_wr(to_integer(" + expr + ") mod 4) <= '1';")
        elif inst.width() == 2:
          tw.writeLine("m_wr((to_integer(" + expr + ") mod 2)*2) <= '1';")
          tw.writeLine("m_wr(((to_integer(" + expr + ") mod 2)*2)+1) <= '1';")
        elif inst.width() == 4:
          tw.writeLine("m_wr <= \"1111\";")
        else:
          raise ValueError("Invalid width " + str(inst.width()) + " while translating instruction " + str(inst) + ".")

      tw.writeBlankLine()

    # Otherwise, this is a computation state, and we need to emit translations of
    # each instruction.
    else:
      # First get all inputs to the block.
      tw.writeCommentLine("Inputs: " + ", ".join(list(map(lambda r: "r{:02d}".format(r),
                                                           s.inputs()))))
      for i in s.inputs():
        if i != 0:
          tw.writeLine(localName(s.name(), i) + " := " + "r{:02d}".format(i) + ";")

      tw.writeBlankLine()

      # Now write translations of all the instructions in the block.
      for inst in s.instructions():
        tw.writeCommentLine(str(inst))
        for line in translateInstruction(s.name(), inst):
          tw.writeLine(line)
        tw.writeBlankLine()

      tw.writeBlankLine()

      # Finally, write locals to their respective permanent registers.
      tw.writeCommentLine("Outputs: " + ", ".join(list(map(lambda r: "r{:02d}".format(r),
                                                           s.outputs()))))
      for o in s.outputs():
        if o != 0:
          tw.writeLine("r{:02d}".format(o) + " <= " + localName(s.name(), o) + ";")

      tw.writeBlankLine()

    # We transition to the next state if this is not a wait state.
    if "CLK" in s.triggers() and s.getTransition("CLK") != s:
      tw.writeLine("int_state <= " + s.getTransition("CLK").name() + ";")

    tw.decreaseIndent()

  tw.writeLine("when others => null;")
  tw.writeLine("end case;")

  tw.decreaseIndent()

  # Now do M_RDY rising edge transitions (i.e. memory accesses.)
  tw.writeLine("elsif rising_edge(m_rdy) then")

  tw.increaseIndent()
  tw.writeLine("m_wr <= \"0000\";")
  tw.writeLine("m_rd <= '0';")
  tw.writeBlankLine()

  firstState = True
  tw.writeLine("case int_state is")

  for i in range(len(stateMachine)):
    s = stateMachine[i]

    if s.isWaitState():
      tw.writeLine("when " + s.name() + " =>")

      tw.increaseIndent()

      # If the wait is a READ, we need to get the data from memory into the correct register.
      if s.instruction().isRead():
        inst = s.instruction()

        tw.writeCommentLine("Read data into r{:02d}.".format(inst.rD()))

        if inst.width() == 1:
          tw.writeCommentLine("Loading byte.")
          tw.writeLine("r{:02d} <= (others => '0');")
          tw.writeLine("r{:02d}(7 downto 0) <= signed(m_data_in)((offset+7) downto offset);")
        elif inst.width() == 2:
          tw.writeCommentLine("Loading halfword.")
          tw.writeLine("r{:02d} <= (others => '0');")
          tw.writeLine("r{:02d}(15 downto 0) <= signed(m_data_in)((offset+15) downto offset);")
        elif inst.width() == 4:
          tw.writeLine("r{:02d}".format(inst.rD()) + " <= signed(m_data_in);")
        else:
          raise ValueError("Invalid width " + str(inst.width()) + " while translating instruction " + str(inst) + ".")

        tw.writeBlankLine()

      tw.writeLine("int_state <= " + s.getTransition("M_RDY").name() + ";")

      tw.writeBlankLine()
      tw.decreaseIndent()

  tw.writeLine("when others => null;")
  tw.writeLine("end case;")

  tw.decreaseIndent()
  tw.writeLine("end if;")

  tw.decreaseIndent()

  tw.writeLine("else")

  tw.increaseIndent()

  tw.writeCommentLine("Put outputs into tri-state to avoid conflicts.")

  tw.writeLine("m_data_out <= (others => 'Z');")
  tw.writeLine("m_addr     <= (others => 'Z');")

  tw.writeBlankLine()

  for out in stateMachine.outputRegisters():
    tw.writeLine("out_r{:02d} <= (others => 'Z');".format(out))

  tw.writeBlankLine()

  tw.writeLine("m_rd       <= 'Z';")
  tw.writeLine("m_wr       <= \"ZZZZ\";")

  tw.decreaseIndent()

  tw.writeLine("end if;")

  tw.decreaseIndent()
  tw.writeLine("end process;")

  tw.decreaseIndent()
  tw.writeLine("end " + entityName + "_behav;")

  return str(tw)

def getComponentDefinition(stateMachine):
  # Write component statement.
  tw = text.TextWriter(4, "--")
  tw.increaseIndent()

  entityName = "hw_core_" + stateMachine.name()
  tw.writeLine("component " + entityName + " is")

  # Write port definitions.
  tw.increaseIndent()
  tw.writeLine("port (")
  tw.increaseIndent()

  ports = getPorts(stateMachine)
  for port in ports[:-1]:
    tw.writeLine(port[0] + " : " + port[1] + " " + port[2] + ";")

  tw.writeLine(ports[-1][0] + " : " + ports[-1][1] + " " + ports[-1][2])

  tw.decreaseIndent()
  tw.writeLine(");")

  tw.decreaseIndent()
  tw.writeLine("end component " + entityName + ";")
  tw.decreaseIndent()
  tw.writeBlankLine()

  return str(tw)

def getUUTDefinition(stateMachine):
  tw = text.TextWriter(4, "--")

  tw.increaseIndent()
  entityName = "hw_core_" + stateMachine.name()
  tw.writeLine(stateMachine.name() + "_uut : " + entityName + " port map")
  tw.writeLine("(")

  tw.increaseIndent()

  ports = getPorts(stateMachine)
  for port in ports[:-1]:
    actualName = port[3]
    tw.writeLine(port[0] + " => " + actualName + ",")

  tw.writeLine(ports[-1][0] + " => " + ports[-1][3])

  tw.decreaseIndent()
  tw.writeLine(");")
  tw.writeBlankLine()

  return str(tw)

def getTestbenchSignals(stateMachine):
  tw = text.TextWriter(4, "--")

  tw.increaseIndent()

  for port in getPorts(stateMachine):
    if port[0] == "rst" or port[0] == "done" or port[0] == "sel":
      tw.writeLine("signal " + stateMachine.name() + "_" + port[0] + " : " + port[2] + ";")

  tw.writeBlankLine()
  tw.decreaseIndent()

  return str(tw)

def getControllerWriteRegisters(stateMachines):
  tw = text.TextWriter(4, "--")
  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()

  tw.writeLine("when x\"44A00000\" =>")
  tw.increaseIndent()
  tw.writeLine("case M_AXI_DP_0_wdata is")
  for i in range(0, 32):
    if i < len(stateMachines):
      tw.writeCommentLine("Select accelerator " + stateMachines[i].name() + ".")
      tw.writeLine("when x\"{:08x}\" =>".format(2**stateMachines[i].id()))
      tw.increaseIndent()
      tw.writeLine(stateMachines[i].name() + "_sel <= '1';")
      tw.writeLine("int_state <= S_WAITING_FOR_CORE;")
      tw.writeBlankLine()
      tw.decreaseIndent()

  tw.writeCommentLine("A non-one-hot value is undefined behaviour.")
  tw.writeLine("when others => null;")
  tw.writeBlankLine()
  tw.writeLine("end case;")
  tw.writeBlankLine()
  tw.decreaseIndent()

  for i in range(1,32):
    tw.writeLine("when x\"44A0{:04x}\" =>".format((i)*4))
    tw.increaseIndent()
    tw.writeLine("reg_to_accel_{:02d} <= M_AXI_DP_0_wdata;".format(i))
    tw.decreaseIndent()

  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()

  return str(tw)

def getControllerReadRegisters(stateMachines):
  tw = text.TextWriter(4, "--")
  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()

  tw.writeLine("when x\"44A00000\" =>")
  tw.increaseIndent()
  tw.writeCommentLine("Reset all state machines.")
  for sm in stateMachines:
    tw.writeLine(sm.name() + "_rst <= '1';")
    tw.writeLine(sm.name() + "_sel <= '0';")

  tw.writeBlankLine()
  tw.writeCommentLine("Put controller into READY state.")
  tw.writeLine("int_state <= S_READY;")
  tw.decreaseIndent()

  for i in range(1,32):
    tw.writeLine("when x\"44A0{:04x}\" =>".format((i)*4))
    tw.increaseIndent()
    tw.writeLine("M_AXI_DP_0_rdata <= reg_from_accel_{:02d};".format(i))
    tw.decreaseIndent()

  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()

  return str(tw)

def getControllerResetPorts(stateMachines):
  ports = []

  for sm in stateMachines:
    ports.append((sm.name() + "_rst", "out"))

  return ports

def getControllerSelectPorts(stateMachines):
  ports = []

  for sm in stateMachines:
    ports.append((sm.name() + "_sel", "out"))

  return ports

def getControllerDonePorts(stateMachines):
  ports = []

  for sm in stateMachines:
    ports.append((sm.name() + "_done", "in"))

  return ports

def getControllerUnreset(stateMachines):
  tw = text.TextWriter(4, "--")

  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()

  for sm in stateMachines:
    tw.writeLine(sm.name() + "_rst <= '0';")

  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()

  return str(tw)

def getControllerStateMachinesDone(stateMachines):
  tw = text.TextWriter(4, "--")

  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()

  for sm in stateMachines:
    tw.writeLine("if " + sm.name() + "_done = '1' then")
    tw.increaseIndent()
    tw.writeLine("int_state <= S_DONE;")
    tw.decreaseIndent()
    tw.writeLine("end if;")

  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()
  tw.decreaseIndent()

  return str(tw)

def reportAcceleratorStart(stateMachines):
  tw = text.TextWriter(4, "--")

  tw.increaseIndent()
  tw.increaseIndent()
  tw.increaseIndent()

  for sm in stateMachines:
    tw.writeLine("if " + sm.name() + "_sel = '1' and accel_started = '0' then")
    tw.increaseIndent()
    tw.writeLine("report \"TESTBENCH: " + sm.name() + " EXECUTION START.\";")
    tw.writeLine("accel_started <= '1';")
    tw.decreaseIndent()
    tw.writeLine("elsif " + sm.name() + "_done = '1' and accel_started = '1' then")
    tw.increaseIndent()
    tw.writeLine("report \"TESTBENCH: " + sm.name() + " EXECUTION COMPLETE.\";")
    tw.writeLine("accel_started <= '0';")
    tw.decreaseIndent()
    tw.writeLine("end if;")
    tw.writeBlankLine()

  return str(tw)

def localName(stateName, register):
  # Use the global constant for r0.
  if register == 0:
    return "r00"
  else:
    return "{:s}_r{:02d}".format(stateName, register)

# Translates a given instruction into one or more lines of VHDL.
def translateInstruction(stateName, instruction):
  mnemonic = instruction.mnemonic()

  lines = []
  needsTemp = False

  if instruction.imm() != None:
    immediate = str(instruction.imm())
  elif instruction.label() != None:
    immediate = "%%SYM_" + instruction.label() + "%%"

  if mnemonic == "addk":
    lines.append(ADD_FORMAT.format(localName(stateName, instruction.rD()),
                                   localName(stateName, instruction.rA()),
                                   localName(stateName, instruction.rB())))
  elif mnemonic == "addik":
    lines.append(ADDI_FORMAT.format(localName(stateName, instruction.rD()),
                                    localName(stateName, instruction.rA()),
                                    immediate))

  elif mnemonic == "mul":
    # A 32-bit multiply produces a 64-bit result, so we put the result in a 64-bit temporary variable
    # and then put the lower 32 bits of that variable into the destination register.
    # The generated circuit is the same, but this appeases the VHDL typing gods.
    lines.append(MUL_FORMAT.format("temp64",
                                   localName(stateName, instruction.rA()),
                                   localName(stateName, instruction.rB())))

    needsTemp = True

  elif mnemonic == "muli":
    # A 32-bit multiply produces a 64-bit result, so we put the result in a 64-bit temporary variable
    # and then put the lower 32 bits of that variable into the destination register.
    # The generated circuit is the same, but this appeases the VHDL typing gods.
    lines.append(MULI_FORMAT.format("temp64",
                                   localName(stateName, instruction.rA()),
                                   immediate))

    needsTemp = True

  elif mnemonic == "and":
    lines.append(AND_FORMAT.format(localName(stateName, instruction.rD()),
                                   localName(stateName, instruction.rA()),
                                   localName(stateName, instruction.rB())))

  elif mnemonic == "andi":
    lines.append(ANDI_FORMAT.format(localName(stateName, instruction.rD()),
                                    localName(stateName, instruction.rA()),
                                    immediate))

  elif mnemonic == "or":
    lines.append(OR_FORMAT.format(localName(stateName, instruction.rD()),
                                  localName(stateName, instruction.rA()),
                                  localName(stateName, instruction.rB())))

  elif mnemonic == "ori":
    lines.append(ORI_FORMAT.format(localName(stateName, instruction.rD()),
                                   localName(stateName, instruction.rA()),
                                   immediate))

  elif mnemonic == "xor":
    lines.append(XOR_FORMAT.format(localName(stateName, instruction.rD()),
                                   localName(stateName, instruction.rA()),
                                   localName(stateName, instruction.rB())))

  elif mnemonic == "xori":
    lines.append(XORI_FORMAT.format(localName(stateName, instruction.rD()),
                                    localName(stateName, instruction.rA()),
                                    immediate))

  elif mnemonic == "srl":
    lines.append(SRL_FORMAT.format(localName(stateName, instruction.rD()),
                                   localName(stateName, instruction.rA())))

  else:
    raise ValueError("Unknown instruction for translation: " + str(instruction))

  if needsTemp:
    lines.append(localName(stateName, instruction.rD()) + " := temp64(31 downto 0);")

  return lines

def getPorts(stateMachine):
  ports = []

  # CLK, M_RDY, and RST signals.
  ports.append(("clk", "in", "std_logic", "clk"))
  ports.append(("rst", "in", "std_logic", stateMachine.name() + "_rst"))
  ports.append(("m_rdy", "in", "std_logic", "m_rdy"))

  # Read and write strobes.
  ports.append(("m_wr", "out", "std_logic_vector(3 downto 0)", "m_wr"))
  ports.append(("m_rd", "out", "std_logic", "m_rd"))

  # Memory address and data lines.
  ports.append(("m_addr", "out", "std_logic_vector(31 downto 0)", "m_addr"))
  ports.append(("m_data_in", "in", "std_logic_vector(31 downto 0)", "m_data_to_accel"))
  ports.append(("m_data_out", "out", "std_logic_vector(31 downto 0)", "m_data_from_accel"))

  # Inputs for each register.
  for r in stateMachine.inputRegisters():
    if r != 0:
      ports.append(("in_r{:02d}".format(r), "in", "std_logic_vector(31 downto 0)", "reg_to_accel_{:02d}".format(r)))

  # Outputs for each register.
  for r in stateMachine.outputRegisters():
    if r != 0:
      ports.append(("out_r{:02d}".format(r), "out", "std_logic_vector(31 downto 0)", "reg_from_accel_{:02d}".format(r)))

  # Done signal.
  ports.append(("done", "out", "std_logic", stateMachine.name() + "_done"))

  # Select signal.
  ports.append(("sel", "in", "std_logic", stateMachine.name() + "_sel"))

  return ports
