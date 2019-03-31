from . import basicblocks
from parsing import instructions

STATE_NAME_FORMAT = "S_{:03d}"

class StateMachine:
  def __init__(self, name, basicBlock):
    self._name = name
    self._inputRegisters = basicBlock.inputs()
    self._outputRegisters = basicBlock.outputs()
    self._usedRegisters = basicBlock.used()

    self._block = basicBlock

    self._states = getStates(basicBlock)
    linkStates(self._states)

    self._usesCarry = False
    for s in self._states:
      if s.usesCarry():
        self._usesCarry = True

  def __len__(self):
    return len(self._states)

  def __getitem__(self, index):
    return self._states[index]

  def name(self):
    return self._name

  def id(self):
    return self._id

  def setId(self, id):
    self._id = id

  def block(self):
    return self._block

  def inputRegisters(self):
    return self._inputRegisters

  def outputRegisters(self):
    return self._outputRegisters

  def usedRegisters(self):
    return self._usedRegisters

  def cost(self):
    return (len(self.inputRegisters()) + len(self.outputRegisters()) + len(self)) / len(self._block)

  def replacementInstructions(self):
    replace = []

    controllerPointer = 13
    tempRegister = 31
    idRegister = 30

    # Put MSR in temp register if we need it.
    if self._usesCarry:
      replace.append(instructions.SystemInstruction("mfs", "msr", None, tempRegister, None, None, None, None, False))

    # Put ID in ID register.
    replace.append(instructions.IntegerArithmeticInstruction("addik", 0, None, idRegister, self._id, None, None, None, False))

    # To take advantage of AXI pipelining, all writes are in a single burst.

    # Write the input registers to the right ports.
    # We just exclude r13, r30 and r31 because we ensure that the compiler doesn't use those registers
    # through the -ffixed option.
    for i in sorted(self.inputRegisters()):
      if i != controllerPointer and i != tempRegister and i != idRegister:
        replace.append(instructions.OutputInstruction("swi", controllerPointer, None, i, i*4, None, None, 4, False))

    # Get MSR and write to controller, if the core modifies the carry flag.
    if self._usesCarry:
      replace.append(instructions.OutputInstruction("swi", controllerPointer, None, tempRegister, 31*4, None, None, 4, False))

    # Write to the special controller register that will start our desired state machine.
    replace.append(instructions.OutputInstruction("swi", controllerPointer, None, idRegister, 0, None, None, 4, False))

    # Go to sleep until wakeup signal from controller.
    replace.append(instructions.SystemInstruction("mbar", None, None, None, 24, None, None, None, False))

    # Read the output registers from the right ports.
    for o in sorted(self.outputRegisters()):
      if o != controllerPointer and o != tempRegister and o != idRegister:
        replace.append(instructions.InputInstruction("lwi", controllerPointer, None, o, o*4, None, None, 4, False))

    # Read the special port at offset 0 to reset the controller.
    # This also gets us the updated MSR register.
    replace.append(instructions.InputInstruction("lwi", controllerPointer, None, tempRegister, 0, None, None, 4, False))

    if self._usesCarry:
      replace.append(instructions.SystemInstruction("mts", tempRegister, None, "msr", None, None, None, None, False))

    return replace

  def toTikzDef(self):
    nodes = ""

    edges = ""

    previousState = None

    for state in self._states:
      options = ["state"]

      if state.isStartState():
        options.append("initial")

      if previousState != None:
        if state.isWaitState():
          if previousState.isWaitState():
            options.append("below of=" + previousState.name())
          else:
            options.append("below right of=" + previousState.name())
        else:
          if previousState.isWaitState():
            options.append("left of=" + previousState.name())
          else:
            options.append("below of=" + previousState.name())

      nodes += "  \\node[" + ", ".join(options) + "] (" + state.name() + ") {" + escapeUnderscore(state.name()) + "};\n"

      for trigger in state.triggers():
        destinationState = state.getTransition(trigger)

        if destinationState == state:
          option = "loop right"
        else:
          if destinationState.isWaitState() and state.isWaitState():
            option = "right"
          elif state.isWaitState():
            option = "above"
          elif destinationState.isWaitState():
            option = "above right"
          else:
            option = "left"

        edges += "  \\draw (" + state.name() + ") edge[" + option + "] node{" + escapeUnderscore(trigger) + "} (" + destinationState.name() + ");\n"

      previousState = state

    definition = "\\begin{tikzpicture}\n" + nodes + "\n" + edges + "\\end{tikzpicture}\n"

    return definition

class State:
  def __init__(self, name):
    self._name = name
    self._transitions = {}
    self._usesCarry = False

  def __str__(self):
    s = "State: " + str(self._name) + "\n"
    s += "Transitions:\n"

    for trigger in self._transitions.keys():
      s += "\t" + str(trigger) + ": " + self._transitions[trigger].name() + "\n"

    return s

  def name(self):
    return self._name

  def isWaitState(self):
    return False

  def isStartState(self):
    return False

  def isEndState(self):
    return False

  def addTransition(self, trigger, state):
    if trigger in self._transitions.keys():
      raise ValueError("Trigger " + str(trigger) + " given is already a transition.")

    self._transitions[trigger] = state

  def getTransition(self, trigger):
    if trigger not in self._transitions.keys():
      raise KeyError("Trigger " + str(trigger) + " is not a trigger in this state.")

    return self._transitions[trigger]

  def triggers(self):
    return self._transitions.keys()

  def locals(self):
    return []

  def usesCarry(self):
    return self._usesCarry

class ComputationState(State):
  def __init__(self, name, instructions):
    super(ComputationState, self).__init__(name)

    self._instructions = instructions

    for i in self._instructions:
      if i.usesCarry():
        self._usesCarry = True

  def __str__(self):
    s = super(ComputationState, self).__str__()

    s += "Computation:\n"

    s += "Inputs: "
    s += "Outputs: "

    for i in self._instructions:
      s += str(i) + "\n"

    return s

  def inputs(self):
    inputs = []
    outputs = []

    for i in self._instructions:
      if i.rA() != None and i.rA() not in inputs and i.rA() not in outputs:
        inputs.append(i.rA())
      if i.rB() != None and i.rB() not in inputs and i.rB() not in outputs:
        inputs.append(i.rB())
      if i.rD() != None and i.rD() not in outputs:
        outputs.append(i.rD())

    return inputs

  def locals(self):
    l = []

    for i in self._instructions:
      if i.rA() != None and i.rA() not in l:
        l.append(i.rA())
      if i.rB() != None and i.rB() not in l:
        l.append(i.rB())
      if i.rD() != None and i.rD() not in l:
        l.append(i.rD())

    return l

  def outputs(self):
    outputs = []

    for i in self._instructions:
      if i.rD() != None and i.rD() not in outputs:
        outputs.append(i.rD())

    return outputs

  def instructions(self):
    return self._instructions

class WaitState(State):
  def __init__(self, name, instruction):
    super(WaitState, self).__init__(name)

    self._instruction = instruction

  def __str__(self):
    s = super(WaitState, self).__str__()
    s += "Wait:\n" + str(self._instruction)

    return s

  def isWaitState(self):
    return True

  def instruction(self):
    return self._instruction

class StartState(State):
  def __init__(self, name, inputs):
    super(StartState, self).__init__(name)

    self._inputs = inputs

  def __str__(self):
    s = super(StartState, self).__str__()
    s += "Inputs: " + ", ".join(list(map(lambda i: "r" + str(i), self._inputs))) + "\n"

    return s

  def isStartState(self):
    return True

class EndState(State):
  def __init__(self, name, outputs):
    super(EndState, self).__init__(name)

    self._outputs = outputs

  def __str__(self):
    s = super(EndState, self).__str__()
    s += "Outputs: " + ", ".join(list(map(lambda i: "r" + str(i), self._outputs))) + "\n"

    return s

  def isEndState(self):
    return True

def getStateMachine(basicBlock):
  return StateMachine(basicBlock.name(), basicBlock)

def escapeUnderscore(s):
  return s.replace("_", "\\_")

def getStates(basicBlock):
  states = []

  states.append(StartState("S_START", basicBlock.inputs()))

  stateNum = 0

  block = []
  for i in basicBlock.lines():
    inst = basicBlock[i]

    if inst.isMemoryAccess():
      if len(block) > 0:
        states.append(ComputationState(STATE_NAME_FORMAT.format(stateNum), block))
        stateNum += 1
      states.append(WaitState(STATE_NAME_FORMAT.format(stateNum), inst))
      stateNum +=1
      block = []
    else:
      block.append(inst)

  if len(block) > 0:
    states.append(ComputationState(STATE_NAME_FORMAT.format(stateNum), block))

  states.append(EndState("S_END", basicBlock.outputs()))

  return states

def linkStates(states):
  i = len(states) - 1

  while i >= 0:
    if states[i].isWaitState():
      states[i].addTransition("CLK", states[i])

    if (i+1) < len(states):
      if states[i].isWaitState():
        trigger = "M_RDY"
      else:
        trigger = "CLK"

      states[i].addTransition(trigger, states[i+1])

    i -= 1
