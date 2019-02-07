STATE_NAME_FORMAT = "S_{:03d}"

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
  states = getStates(basicBlock)
  linkStates(states)

  return states

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
      states[i].addTransition("rising(CLK)", states[i])

    if (i+1) < len(states):
      if states[i].isWaitState():
        trigger = "rising(M_RDY)"
      else:
        trigger = "rising(CLK)"

      states[i].addTransition(trigger, states[i+1])

    i -= 1
