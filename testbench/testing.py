import os
import shutil
import re

import templating
from toolchain import compiler, memory, vivado

from parsing import parser
from analysis import basicblocks

TESTING_DIR = os.path.abspath("testbench")
TEMPLATE_DIR = os.path.abspath("templates")

TESTBENCH_MSG_FORMAT = re.compile("Note: TESTBENCH: (.+)")
PASSED = "!!!PASSED!!!"
FAILED = "!!!FAILED!!!"

def runTest(logger, testName, runSimulation):
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
    generateStateMachines(logger)

    # Compile test harness files.
    compileHarness(logger)

    # Write the memory initialization file.
    writeMemoryInitFile()

    # Generate testbench templates.
    generateTemplates(logger)

    # Run the Vivado simulation if we've been asked to.
    if runSimulation:
        if runVivadoSimulation():
            logger.info("Test " + testName + ": passed.")
        else:
            logger.warn("Test " + testName + ": FAILED.")
    else:
        logger.info("Test " + testName + ": SIMULATION SKIPPED.")

    # Move back to the root directory.
    os.chdir(origDir)

def compileApplication(logger):
    compiler.compile(logger, ["application.c"], "application.s")

def generateStateMachines(logger):
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

  for b in blocks:
    print(b)

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

def generateTemplates(logger):
  # Read the ELF symbols.
  syms = compiler.getElfSymbols(logger, "main.elf")

  vars_testbench = {
    "FAILED_ADDR": syms["test_failed"],
    "PASSED_ADDR": syms["test_passed"]
  }

  # Generate testbench template.
  tbTemplate = os.path.join(TEMPLATE_DIR, "testbench.vhd")
  tclTemplate = os.path.join(TEMPLATE_DIR, "simulate.tcl")
  memTemplate = os.path.join(TEMPLATE_DIR, "memory.vhd")

  templating.processTemplate(tbTemplate, "testbench.vhd", vars_testbench)
  templating.processTemplate(tclTemplate, "simulate.tcl", {})

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
