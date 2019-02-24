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
PASSED = "!!!PASSED!!!"
FAILED = "!!!FAILED!!!"

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
    generateTemplates(logger, selected)

    # Run the Vivado simulation if we've been asked to.
    if runSimulation:
        if runVivadoSimulation():
            logger.info("Test " + testName + ": passed. (" + str(actualNum) + " state machines generated.)")
        else:
            logger.warn("Test " + testName + ": FAILED. (" + str(actualNum) + " state machines generated.)")
    else:
        logger.info("Test " + testName + ": SIMULATION SKIPPED. (" + str(actualNum) + " state machines generated.)")

    # Move back to the root directory.
    os.chdir(origDir)

def compileApplication(logger):
    compiler.compile(logger, ["application.c"], "application.s")

def generateStateMachines(logger, num):
  logger.info("Reading application file...")
  with open("application.s", 'r') as file:
    stream = parser.parse(file.readlines())

  logger.info("Read " + str(stream.instructionCount())
                      + " instructions, "
                      + str(stream.labelCount())
                      + " labels, "
                      + str(stream.directiveCount())
                      + " directives.")

  # Get basic blocks from stream.
  blocks = basicblocks.extractBasicBlocks(logger, stream)

  stateMachines = []
  for b in blocks:
    sm = statemachine.getStateMachine(b)
    stateMachines.append(sm)

  stateMachines = sorted(list(filter(lambda s: s.cost() <= 0, stateMachines)), key=lambda s: s.cost())

  if len(stateMachines) <= num:
    logger.debug("Number specified is lower than or equal to number of viable state machines extracted. Selecting all.")
    selected = stateMachines
  else:
    selected = stateMachines[:num]

  for sm in selected:
    logger.debug("Selected: " + sm.name() + " (cost: " + str(sm.cost()) + ", states: " + str(len(sm)) + ")")
    with open(sm.name() + ".vhd", 'w') as file:
      logger.debug("Writing definition for " + sm.name() + " to file " + sm.name() + ".vhd.")
      file.write(translator.translateStateMachine(sm))

  return selected

def compileHarness(logger):
  # Compile the harness and test functions.
  compiler.compile(logger, ["main.c"], "main.s")
  compiler.compile(logger, ["test.c"], "test.s")

  # Link the assembly file with start.s, and make a hex file.
  # Disassemble this file for later reference.
  compiler.link(logger, ["application.s", "test.s", "main.s", "start.s"], "main.elf")
  compiler.makeHex(logger, "main.elf", "main.hex")
  compiler.disassembleElf(logger, "main.elf", "main.asm")

def writeMemoryInitFile():
  # Generate a memory initialization file ('memory.txt') from the hex file.
  memory.writeMemoryFile("memory.txt", "main.hex")

def generateTemplates(logger, selectedStateMachines):
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

  vars_testbench = {
    "FAILED_ADDR": syms["test_failed"],
    "PASSED_ADDR": syms["test_passed"],
    "STATEMACHINE_COMPONENTS": componentDefs,
    "STATEMACHINE_UUTS": uutDefs,
    "STATEMACHINE_SIGNALS": signals
  }

  # Generate testbench template.
  tbTemplate = os.path.join(TEMPLATE_DIR, "testbench.vhd")
  tclTemplate = os.path.join(TEMPLATE_DIR, "simulate.tcl")
  memTemplate = os.path.join(TEMPLATE_DIR, "memory.vhd")

  templating.processTemplate(tbTemplate, "testbench.vhd", vars_testbench)

  vars_tcl = {
    "ADD_STATEMACHINES": "\n".join(list(map(lambda sm: "add_files -fileset sources_1 {:s}.vhd".format(sm.name()), selectedStateMachines))),
    "REMOVE_STATEMACHINES": "\n".join(list(map(lambda sm: "remove_files -fileset sources_1 {:s}.vhd".format(sm.name()), selectedStateMachines)))
  }

  templating.processTemplate(tclTemplate, "simulate.tcl", vars_tcl)

  vars_memory = {
    "MEMORYFILE": os.path.abspath("memory.txt")
  }

  templating.processTemplate(memTemplate, "memory.vhd", vars_memory)

def runVivadoSimulation():
  passed = None
  output = vivado.start_batch("simulate.tcl")

  # Write the full output to a log file.
  with open("simulate.log", 'w') as logfile:
    logfile.write(output)

  output_lines = output.splitlines()
  for l in output_lines:
    m = TESTBENCH_MSG_FORMAT.match(l)
    if m != None:
      print("TESTBENCH: " + m.groups()[0])

      if m.groups()[0] == PASSED:
        passed = True
      elif m.groups()[0] == FAILED:
        passed = False

  if passed == None:
    raise Exception("Could not determine result of test.")

  return passed
