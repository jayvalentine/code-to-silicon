STATE_NAME_FORMAT = "S_{:03d}"

class StateMachine:
  def __init__(self, name, basicBlock):
    self._name = name
    self._inputRegisters = basicBlock.inputs()
    self._outputRegisters = basicBlock.outputs()
    self._usedRegisters = basicBlock.used()

    self._states = getStates(basicBlock)
    linkStates(self._states)

  def __len__(self):
    return len(self._states)

  def __getitem__(self, index):
    return self._states[index]

  def name(self):
    return self._name

  def inputRegisters(self):
    return self._inputRegisters

  def outputRegisters(self):
    return self._outputRegisters

  def usedRegisters(self):
    return self._usedRegisters

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

class ComputationState(State):
  def __init__(self, name, instructions):
    super(ComputationState, self).__init__(name)
    
    self._instructions = instructions

  def __str__(self):
    s = super(ComputationState, self).__str__()

    s += "Computation:\n"

    for i in self._instructions:
      s += str(i) + "\n"

    return s

  def instructions(self):
    return self._instructions

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
  return StateMachine("test", basicBlock)

def escapeUnderscore(s):
  return s.replace("_", "\\_")

def getStates(basicBlock):
  states = []

  states.append(StartState("S_START", basicBlock.inputs()))

  stateNum = 0

  block = []
  for i in range(len(basicBlock)):
    inst = basicBlock.instructions()[i]

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