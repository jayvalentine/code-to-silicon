import os
import shutil
import re

import templating
from toolchain import compiler, memory, vivado

from parsing import parser
from analysis import basicblocks, statemachine
from translation import translator

TESTING_DIR = os.path.abspath("testbench")
TEMPLATE_DIR = os.path.abspath("templates")

TESTBENCH_MSG_FORMAT = re.compile("Note: TESTBENCH: (.+)")

CYCLES_MSG_FORMAT = re.compile("CYCLES: (\d+)")

PASSED = "!!!PASSED!!!"
FAILED = "!!!FAILED!!!"

MEM_MSG_FORMAT = re.compile("Note: BRAM: READ DETECTED: ([0-9A-F]+) ([0-9A-F]+)")

def runTest(logger, testName, numStateMachines, runSimulation):
    # Get test and temp directory paths.
    testDir = os.path.join(TESTING_DIR, testName)
    tempDir = os.path.join(testDir, "temp")

    # If the temp directory already exists, delete it.
    if os.path.isdir(tempDir):
        shutil.rmtree(tempDir)

    os.makedirs(tempDir)

    # Copy everything in the test dir into the temp dir.
    files = [f for f in os.listdir(testDir) if os.path.isfile(os.path.join(testDir, f))]

    for file in files:
        shutil.copy(os.path.join(testDir, file), tempDir)

    # Move to the temp directory.
    origDir = os.getcwd()
    os.chdir(tempDir)

    # Compile application.
    compileApplication(logger)

    # Analyse generated code and produce statemachines.
    selected = generateStateMachines(logger, numStateMachines)
    actualNum = len(selected)

    # Compile test harness files.
    compileHarness(logger)

    # Write the memory initialization file.
    writeMemoryInitFile()

    # Generate testbench templates.
    generateTemplates(logger, testName, selected)

    # Run the Vivado simulation if we've been asked to.
    if runSimulation:
        vivadoResults = runVivadoSimulation(logger)
        if vivadoResults["passed"]:
            logger.info("Test " + testName + ": passed. (" + str(actualNum) + " state machines generated.)")
        else:
            logger.warn("Test " + testName + ": FAILED. (" + str(actualNum) + " state machines generated.)")
    else:
        logger.info("Test " + testName + ": SIMULATION SKIPPED. (" + str(actualNum) + " state machines generated.)")

    # Move back to the root directory.
    os.chdir(origDir)

    # Return metrics to caller.
    metrics = {
      "cycles": vivadoResults["cycles"],
      "coreCount": len(selected),
      "coreInputs": list(map(lambda sm: len(sm.inputRegisters()), selected)),
      "coreOutputs": list(map(lambda sm: len(sm.outputRegisters()), selected))
    }

    return metrics

def compileApplication(logger):
    compiler.compile(logger, ["application.c"], "application.s")

def generateStateMachines(logger, num):
  logger.info("Reading application file...")
  with open("application.s", 'r') as file:
    stream = parser.parse(file.readlines())

  with open("application.s", 'w') as file:
    file.write(str(stream))

  logger.info("Read " + str(stream.instructionCount())
                      + " instructions, "
                      + str(stream.labelCount())
                      + " labels, "
                      + str(stream.directiveCount())
                      + " directives.")

  # Get basic blocks from stream.
  blocks = basicblocks.extractBasicBlocks(logger, stream)

  blocksSorted = sorted(blocks, key=lambda b: b.cost())

  if len(blocksSorted) <= num:
    logger.debug("Number specified is lower than or equal to number of blocks. Selecting all.")
    selected = blocksSorted
  else:
    selected = blocksSorted[:num]

  # Sort in textual order.
  selected = sorted(selected, key=lambda b: b.lines()[0])

  stateMachines = []
  for b in selected:
    sm = statemachine.getStateMachine(b)
    stateMachines.append(sm)

  id = 0
  change = 0
  for sm in stateMachines:
    sm.setId(id)

    logger.debug("Selected: " + sm.name() + " (cost: " + str(sm.cost()) + ", states: " + str(len(sm)) + ", id: " + str(id) + ")")
    with open(sm.name() + "_temp.vhd", 'w') as file:
      logger.debug("Writing definition for " + sm.name() + " to file " + sm.name() + "_temp.vhd.")
      file.write(translator.translateStateMachine(sm))

    change += stream.replaceLines(sm.block().lines()[0]+change, sm.block().lines()[-1]+change, sm.replacementInstructions())
    id += 1

  with open("application_new.s", 'w') as file:
    file.write(str(stream))

  return stateMachines

def compileHarness(logger):
  # Compile the harness and test functions.
  compiler.compile(logger, ["main.c"], "main.s")
  compiler.compile(logger, ["test.c"], "test.s")

  # Link the assembly file with start.s, and make a hex file.
  # Disassemble this file for later reference.
  compiler.link(logger, ["application_new.s", "test.s", "main.s", "start.s"], "main.elf")
  compiler.makeHex(logger, "main.elf", "main.hex")
  compiler.disassembleElf(logger, "main.elf", "main.asm")

def writeMemoryInitFile():
  # Generate a memory initialization file ('memory.txt') from the hex file.
  memory.writeMemoryFile("memory.txt", "main.hex")

def generateTemplates(logger, testName, selectedStateMachines):
  # Read the ELF symbols.
  syms = compiler.getElfSymbols(logger, "main.elf")

  # Get the component definitions for each state machine.
  componentDefs = ""
  uutDefs = ""
  signals = ""

  for sm in selectedStateMachines:
    componentDefs += translator.getComponentDefinition(sm)
    uutDefs += translator.getUUTDefinition(sm)
    signals += translator.getTestbenchSignals(sm)

    vars_sm = {}
    for sym in syms.keys():
      vars_sm["SYM_" + sym] = str(int(syms[sym], 16))

    templating.processTemplate(sm.name() + "_temp.vhd", sm.name() + ".vhd", vars_sm)

  portDefs = ""
  resetPortSets = ""
  selPortSets = ""

  portsMap = ""

  resetPorts = translator.getControllerResetPorts(selectedStateMachines)

  for port in resetPorts:
    portDefs += "        " + port[0] + " : " + port[1] + " std_logic;\n"
    resetPortSets += "            " + port[0] + " <= '1';\n"
    portsMap += "        " + port[0] + " => " + port[0] + ",\n"

  selPorts = translator.getControllerSelectPorts(selectedStateMachines)

  for port in selPorts:
    portDefs += "        " + port[0] + " : " + port[1] + " std_logic;\n"
    selPortSets += "            " + port[0] + " <= '0';\n"
    portsMap += "        " + port[0] + " => " + port[0] + ",\n"

  donePorts = translator.getControllerDonePorts(selectedStateMachines)

  for port in donePorts:
    portDefs += "        " + port[0] + " : " + port[1] + " std_logic;\n"
    portsMap += "        " + port[0] + " => " + port[0] + ",\n"

  reportStart = translator.reportAcceleratorStart(selectedStateMachines)

  vars_testbench = {
    "FAILED_ADDR": syms["test_failed"],
    "PASSED_ADDR": syms["test_passed"],
    "STATEMACHINE_COMPONENTS": componentDefs,
    "STATEMACHINE_UUTS": uutDefs,
    "STATEMACHINE_SIGNALS": signals,
    "STATEMACHINE_PORTS": portDefs,
    "REPORT_ACCEL_START": reportStart,
    "STATEMACHINE_PORTS_MAP": portsMap,
    "TESTNAME": testName
  }

  # Generate testbench template.
  tbTemplate = os.path.join(TEMPLATE_DIR, "testbench.vhd")
  tclTemplate = os.path.join(TEMPLATE_DIR, "simulate.tcl")
  memTemplate = os.path.join(TEMPLATE_DIR, "memory.vhd")
  controllerTemplate = os.path.join(TEMPLATE_DIR, "hw_accel_controller.vhd")

  templating.processTemplate(tbTemplate, "testbench.vhd", vars_testbench)

  vars_tcl = {
    "ADD_STATEMACHINES": "\n".join(list(map(lambda sm: "add_files -fileset sources_1 {:s}.vhd".format(sm.name()), selectedStateMachines))),
    "REMOVE_STATEMACHINES": "\n".join(list(map(lambda sm: "remove_files -fileset sources_1 {:s}.vhd".format(sm.name()), selectedStateMachines))),
    "TESTNAME": testName
  }

  templating.processTemplate(tclTemplate, "simulate.tcl", vars_tcl)

  vars_memory = {
    "MEMORYFILE": os.path.abspath("memory.txt")
  }

  templating.processTemplate(memTemplate, "memory.vhd", vars_memory)

  writesToRegisters = translator.getControllerWriteRegisters(selectedStateMachines)
  readsFromRegisters = translator.getControllerReadRegisters(selectedStateMachines)

  unreset = translator.getControllerUnreset(selectedStateMachines)
  stateMachinesDone = translator.getControllerStateMachinesDone(selectedStateMachines)

  vars_controller = {
    "WRITE_REG_TO_ACCEL": writesToRegisters,
    "READ_REG_FROM_ACCEL": readsFromRegisters,
    "RESET_STATEMACHINES": resetPortSets,
    "DESELECT_STATEMACHINES": selPortSets,
    "UNRESET_STATEMACHINES": unreset,
    "STATEMACHINE_PORTS": portDefs,
    "STATEMACHINES_DONE": stateMachinesDone
  }

  templating.processTemplate(controllerTemplate, "controller.vhd", vars_controller)

def runVivadoSimulation(logger):
  passed = None
  output = vivado.start_batch("simulate.tcl")

  mem = {}

  cycles = None

  # Write the full output to a log file.
  with open("simulate.log", 'w') as logfile:
    logfile.write(output[1])

  output_lines = output[1].splitlines()
  for l in output_lines:
    m = TESTBENCH_MSG_FORMAT.match(l)
    if m != None:
      logger.info("TESTBENCH: " + m.groups()[0])

      if m.groups()[0] == PASSED:
        passed = True
      elif m.groups()[0] == FAILED:
        passed = False
      else:
        cm = CYCLES_MSG_FORMAT.match(m.groups()[0])
        if cm != None:
          cycles = int(cm.groups()[0])

    else:
      m = MEM_MSG_FORMAT.match(l)
      if m != None:
        logger.debug(l)
        mem[int(m.groups()[0], 16)] = m.groups()[1]

  with open("memdump.txt", 'w') as memdump:
    for i in range(0, 2048):
      addr = i*4
      if addr in mem.keys():
        memdump.write("{:08x}: {:s} {:s} {:s} {:s}\n".format(addr, mem[addr][6:], mem[addr][4:6], mem[addr][2:4], mem[addr][0:2]))

  if passed == None:
    raise Exception("Could not determine result of test.")

  results = {
    "passed": passed,
    "cycles": cycles
  }

  return results
