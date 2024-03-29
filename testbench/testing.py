import os
import shutil
import re
import time
import math

import templating
from toolchain import compiler, memory, vivado

from parsing import parser
from analysis import basicblocks, statemachine
from translation import translator

TESTING_DIR = os.path.abspath("testbench")
TEMPLATE_DIR = os.path.abspath("templates")
SIM_DIR = os.path.abspath("microblaze_system/microblaze_system.sim/sim_1")

TESTBENCH_MSG_FORMAT = re.compile("Note: TESTBENCH: (.+)")

CYCLES_MSG_FORMAT = re.compile("CYCLES:\s+(\d+)")
MB_CYCLES_FORMAT = re.compile("MICROBLAZE:\s+(\d+)")
TRANSFER_CYCLES_FORMAT = re.compile("AXI TRANSFER:\s+(\d+)")
CORE_CYCLES_FORMAT = re.compile("CORES:\s+(\d+)")
SLEEP_CYCLES_FORMAT = re.compile("SLEEP OVERHEAD:\s+(\d+)")

CORE_COMPLETE_FORMAT = re.compile("(\S+) EXECUTION COMPLETE: (\d+) CYCLES.")

LUT_UTIL_FORMAT = re.compile("\| Slice LUTs\*\s+\| \s*\d+ \| \s*\d+ \| \s*\d+ \| \s*(\d+\.\d+) \|.*")
REG_UTIL_FORMAT = re.compile("\| Slice Registers\s+\| \s*\d+ \| \s*\d+ \| \s*\d+ \| \s*(\d+\.\d+) \|.*")
MEM_UTIL_FORMAT = re.compile("\| Block RAM Tile\s+\| \s*\d+ \| \s*\d+ \| \s*\d+ \| \s*(\d+\.\d+) \|.*")
DSP_UTIL_FORMAT = re.compile("\| DSPs\s+\| \s*\d+ \| \s*\d+ \| \s*\d+ \| \s*(\d+\.\d+) \|.*")

DYNAMIC_POWER_FORMAT = re.compile("\| Dynamic \(W\)\s+\| (\d+\.\d+)")
STATIC_POWER_FORMAT = re.compile("\| Device Static \(W\)\s+\| (\d+\.\d+)")

PASSED = "!!!PASSED!!!"
FAILED = "!!!FAILED!!!"

MEM_MSG_FORMAT = re.compile("Note: BRAM: READ DETECTED: ([0-9A-F]+) ([0-9A-F]+)")

def runTest(logger, testName, numStateMachines, runSimulation, analysisType, mode):
    # Get test and temp directory paths.
    testDir = os.path.join(TESTING_DIR, testName)
    tempDir = os.path.join(testDir, "temp")

    # If the temp directory already exists, delete it.
    if os.path.isdir(tempDir):
        shutil.rmtree(tempDir, ignore_errors=True)

    os.makedirs(tempDir)

    # If the simulation directory exists, delete it.
    if os.path.isdir(SIM_DIR):
      shutil.rmtree(SIM_DIR, ignore_errors=True)

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
    start = time.time()
    blocks, selected, percentageConverted = generateStateMachines(logger, numStateMachines, analysisType, mode)
    end = time.time()

    logger.info("Analysis completed in " + str(round(end-start, 4)) + "s.")

    memDensities = []
    sizes = []
    inputs = []
    outputs = []
    avgWidths = []
    for b in blocks:
      memDensities.append(b.memoryAccessDensity())
      sizes.append(len(b))
      inputs.append(len(b.inputs()))
      outputs.append(len(b.outputs()))
      avgWidths.append(b.averageComputationWidth())

    actualNum = len(selected)

    # Compile test harness files.
    compileHarness(logger)

    # Write the memory initialization file.
    writeMemoryInitFile()

    # Generate testbench templates.
    generateTemplates(logger, testName, selected)

    logger.info("{:2.2f}% of program converted.".format(percentageConverted * 100))

    # Run the Vivado simulation if we've been asked to.
    if runSimulation:
      vivadoResults = runVivadoSimulation(testName, logger)
      if vivadoResults["passed"]:
          logger.info("Test " + testName + ": passed. (" + str(actualNum) + " state machines generated.)")

          # Delete the synthesis run.
          if os.path.isdir(os.path.join(origDir, "microblaze_system", "microblaze_system.runs", "synth_" + testName)):
            shutil.rmtree(os.path.join(origDir, "microblaze_system", "microblaze_system.runs", "synth_" + testName))

      else:
          logger.warn("Test " + testName + ": FAILED. (" + str(actualNum) + " state machines generated.)")

      logger.info("Total cycles: {:d} (mb {:d}, cores {:d}, axi {:d}, sleep {:d})".format(vivadoResults["cycles"], vivadoResults["cycleBreakdown"][0], vivadoResults["cycleBreakdown"][2], vivadoResults["cycleBreakdown"][1], vivadoResults["cycleBreakdown"][3]))
      logger.info("Utilization: LUTs: {:2.4f}%, Registers: {:2.4f}%, BRAMs: {:2.4f}%, DSPs: {:2.4f}%".format(vivadoResults["util"][0], vivadoResults["util"][1], vivadoResults["util"][2], vivadoResults["util"][3]))
      logger.info("Power Usage: Dynamic: {:2.4f} W, Static: {:2.4f} W".format(vivadoResults["power"][0], vivadoResults["power"][1]))
    else:
      vivadoResults = {
        "passed": None,
        "cycles": None,
        "cycleBreakdown": None,
        "coreExecs": None,
        "util": None,
        "power": None
      }
      logger.info("Test " + testName + ": SIMULATION SKIPPED. (" + str(actualNum) + " state machines generated.)")

    ipc = {}

    for sm in selected:
      if sm.name() in vivadoResults["coreExecs"]:
        c = vivadoResults["coreExecs"][sm.name()]
        ipc[sm.name()] = len(sm.block()) / c

    # Move back to the root directory.
    os.chdir(origDir)

    # Return metrics to caller.
    metrics = {
      "analysisTime": (end-start),
      "result": vivadoResults["passed"],
      "cycles": vivadoResults["cycles"],
      "cycleBreakdown": vivadoResults["cycleBreakdown"],
      "coreExecs": vivadoResults["coreExecs"],
      "dpower": vivadoResults["power"][0],
      "spower": vivadoResults["power"][1],
      "util": vivadoResults["util"],
      "coreIPC": ipc,
      "coreCount": len(selected),
      "coreInputs": list(map(lambda sm: len(sm.inputRegisters()), selected)),
      "coreOutputs": list(map(lambda sm: len(sm.outputRegisters()), selected)),
      "coreStates": list(map(lambda sm: len(sm), selected)),
      "heuristicCost": list(map(lambda sm: sm.block().cost(), selected)),
      "actualCost": list(map(lambda sm: sm.cost(), selected)),
      "blockAvgWidths": avgWidths,
      "blockSize": sizes,
      "blockMemDensity": memDensities,
      "blockInputs": inputs,
      "blockOutputs": outputs,
      "percentageConverted": percentageConverted
    }

    return metrics

def compileApplication(logger):
    compiler.compile(logger, ["application.c"], "application.s")

def generateStateMachines(logger, num, analysisType, mode):
  logger.info("Reading application file...")
  with open("application.s", 'r') as file:
    stream = parser.parse(file.readlines())

  with open("application_parsed.s", 'w') as file:
    file.write(str(stream))

  logger.info("Read " + str(stream.instructionCount())
                      + " instructions, "
                      + str(stream.labelCount())
                      + " labels, "
                      + str(stream.directiveCount())
                      + " directives.")

  # Get basic blocks from stream.
  blocks = basicblocks.extractBasicBlocks(logger, stream, mode)

  # Filter any blocks we don't want to convert.
  blocks = list(filter(lambda b: b.cost() != math.inf, blocks))

  if analysisType == "hybrid":
    logger.info("Selecting blocks based on hybrid cost function.")
    blocksSorted = sorted(blocks, key=lambda b: b.cost())

    if len(blocksSorted) <= num:
      logger.debug("Number specified is lower than or equal to number of blocks. Selecting all.")
      selected = blocksSorted
    else:
      selected = blocksSorted[:num]

    stateMachines = []
    for b in selected:
      sm = statemachine.getStateMachine(b)
      stateMachines.append(sm)

    # Emit info about selected cores in cost order.
    for sm in stateMachines:
      logger.info("Selected: " + sm.name() + " (cost: " + str(round(sm.block().cost(), 4)) + ", states: " + str(len(sm)) + ", inputs: " + str(len(sm.inputRegisters())) + ", outputs: " + str(len(sm.outputRegisters())) + ")")

  elif analysisType == "avgwidth":
    logger.info("Selecting blocks based on potential parallelism (computation width).")
    blocksSorted = sorted(blocks, key=lambda b: b.averageComputationWidth())

    if len(blocksSorted) <= num:
      logger.debug("Number specified is lower than or equal to number of blocks. Selecting all.")
      selected = blocksSorted
    else:
      selected = blocksSorted[:num]

    stateMachines = []
    for b in selected:
      sm = statemachine.getStateMachine(b)
      stateMachines.append(sm)

    # Emit info about selected cores in cost order.
    for sm in stateMachines:
      logger.info("Selected: " + sm.name() + " (average width: " + str(round(sm.block().averageComputationWidth(), 4)) + ", states: " + str(len(sm)) + ", inputs: " + str(len(sm.inputRegisters())) + ", outputs: " + str(len(sm.outputRegisters())) + ")")

  elif analysisType == "memdensity":
    logger.info("Selecting blocks based on memory access density.")
    blocksSorted = sorted(blocks, key=lambda b: b.memoryAccessDensity())

    if len(blocksSorted) <= num:
      logger.debug("Number specified is lower than or equal to number of blocks. Selecting all.")
      selected = blocksSorted
    else:
      selected = blocksSorted[:num]

    stateMachines = []
    for b in selected:
      sm = statemachine.getStateMachine(b)
      stateMachines.append(sm)

    # Emit info about selected cores in cost order.
    for sm in stateMachines:
      logger.info("Selected: " + sm.name() + " (memory access density: " + str(round(sm.block().memoryAccessDensity(), 4)) + ", states: " + str(len(sm)) + ", inputs: " + str(len(sm.inputRegisters())) + ", outputs: " + str(len(sm.outputRegisters())) + ")")

  elif analysisType == "overhead":
    logger.info("Selecting blocks based on I/O overhead.")
    blocksSorted = sorted(blocks, key=lambda b: b.ioOverhead())

    if len(blocksSorted) <= num:
      logger.debug("Number specified is lower than or equal to number of blocks. Selecting all.")
      selected = blocksSorted
    else:
      selected = blocksSorted[:num]

    stateMachines = []
    for b in selected:
      sm = statemachine.getStateMachine(b)
      stateMachines.append(sm)

    # Emit info about selected cores in cost order.
    for sm in stateMachines:
      logger.info("Selected: " + sm.name() + " (I/O overhead: " + str(round(sm.block().ioOverhead(), 4)) + ", states: " + str(len(sm)) + ", inputs: " + str(len(sm.inputRegisters())) + ", outputs: " + str(len(sm.outputRegisters())) + ")")

  # Get the sum of the lengths of all basic blocks.
  sumAll = 0
  for b in blocks:
    sumAll += len(b)

  # Get the sum of the lengths of selected basic blocks.
  sumSelected = 0
  for b in selected:
    sumSelected += len(b)

  # Sort in textual order.
  stateMachines = sorted(stateMachines, key=lambda sm: sm.block().startLine())

  id = 0
  change = 0
  for sm in stateMachines:
    sm.setId(id)

    with open(sm.name() + "_temp.vhd", 'w') as file:
      logger.debug("Writing definition for " + sm.name() + " to file " + sm.name() + "_temp.vhd.")
      file.write(translator.translateStateMachine(sm))

    change += stream.replaceLines(sm.block().lines()[0]+change, sm.block().lines()[-1]+change, sm.replacementInstructions())
    id += 1

  with open("application_new.s", 'w') as file:
    file.write(str(stream))

  return (blocks, stateMachines, (sumSelected/sumAll))

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
    "APPLICATION_ADDR": syms["application"],
    "TEST_ADDR": syms["test"],
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
  synthTemplate = os.path.join(TEMPLATE_DIR, "testbench_synth.vhd")
  tclTemplate = os.path.join(TEMPLATE_DIR, "simulate.tcl")
  memTemplate = os.path.join(TEMPLATE_DIR, "memory_sim.vhd")
  memSynthTemplate = os.path.join(TEMPLATE_DIR, "memory_synth.vhd")
  controllerTemplate = os.path.join(TEMPLATE_DIR, "hw_accel_controller.vhd")

  templating.processTemplate(tbTemplate, "testbench.vhd", vars_testbench)
  templating.processTemplate(synthTemplate, "testbench_synth.vhd", vars_testbench)

  vars_tcl = {
    "ADD_STATEMACHINES": "\n".join(list(map(lambda sm: "add_files -fileset sources_1 {:s}.vhd".format(sm.name()), selectedStateMachines))),
    "REMOVE_STATEMACHINES": "\n".join(list(map(lambda sm: "remove_files -fileset sources_1 {:s}.vhd".format(sm.name()), selectedStateMachines))),
    "TESTNAME": testName,
    "SAIF": os.path.abspath(testName + ".saif"),
    "POWER": os.path.abspath(testName + "-power.txt"),
    "UTIL": os.path.abspath(testName + "-util.txt")
  }

  templating.processTemplate(tclTemplate, "simulate.tcl", vars_tcl)

  vars_memory = {
    "MEMORYFILE": os.path.abspath("memory.txt")
  }

  templating.processTemplate(memTemplate, "memory_sim.vhd", vars_memory)
  templating.processTemplate(memSynthTemplate, "memory_synth.vhd", vars_memory)

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

def runVivadoSimulation(testName, logger):
  passed = None
  output = vivado.start_batch("simulate.tcl")

  mem = {}

  cycles = None
  mb_cycles = None
  axi_cycles = None
  core_cycles = None
  sleep_cycles = None

  core_execs = {}

  output_lines = output[1].splitlines()
  for l in output_lines:
    m = TESTBENCH_MSG_FORMAT.match(l)
    if m != None:
      logger.debug("TESTBENCH: " + m.groups()[0])

      if m.groups()[0] == PASSED:
        passed = True
      elif m.groups()[0] == FAILED:
        passed = False
      else:
        cm = CYCLES_MSG_FORMAT.match(m.groups()[0])
        if cm != None:
          cycles = int(cm.groups()[0])

        cm = MB_CYCLES_FORMAT.match(m.groups()[0])
        if cm != None:
          mb_cycles = int(cm.groups()[0])

        cm = TRANSFER_CYCLES_FORMAT.match(m.groups()[0])
        if cm != None:
          axi_cycles = int(cm.groups()[0])

        cm = CORE_CYCLES_FORMAT.match(m.groups()[0])
        if cm != None:
          core_cycles = int(cm.groups()[0])

        cm = SLEEP_CYCLES_FORMAT.match(m.groups()[0])
        if cm != None:
          sleep_cycles = int(cm.groups()[0])

        cm = CORE_COMPLETE_FORMAT.match(m.groups()[0])
        if cm != None:
          core_execs[cm.groups()[0]] = int(cm.groups()[1])


    else:
      m = MEM_MSG_FORMAT.match(l)
      if m != None:
        logger.debug(l)
        mem[int(m.groups()[0], 16)] = m.groups()[1]

  lut_util = None
  reg_util = None
  mem_util = None
  dsp_util = None

  with open(testName + "-util.txt", "r") as util:
    for line in util.readlines():
      m = LUT_UTIL_FORMAT.match(line)
      if m != None:
        lut_util = float(m.groups()[0])
      else:
        m = REG_UTIL_FORMAT.match(line)
        if m != None:
          reg_util = float(m.groups()[0])
        else:
          m = MEM_UTIL_FORMAT.match(line)
          if m != None:
            mem_util = float(m.groups()[0])
          else:
            m = DSP_UTIL_FORMAT.match(line)
            if m != None:
              dsp_util = float(m.groups()[0])

  dynamic_power = None
  static_power = None

  with open(testName + "-power.txt", "r") as util:
    for line in util.readlines():
      m = DYNAMIC_POWER_FORMAT.match(line)
      if m != None:
        dynamic_power = float(m.groups()[0])
      else:
        m = STATIC_POWER_FORMAT.match(line)
        if m != None:
          static_power = float(m.groups()[0])

  """
  with open("memdump.txt", 'w') as memdump:
    for i in range(0, 2048):
      addr = i*4
      if addr in mem.keys():
        memdump.write("{:08x}: {:s} {:s} {:s} {:s}\n".format(addr, mem[addr][6:], mem[addr][4:6], mem[addr][2:4], mem[addr][0:2]))
  """
  if passed == None:
    raise Exception("Could not determine result of test.")

  results = {
    "passed": passed,
    "cycles": cycles,
    "cycleBreakdown": (mb_cycles, axi_cycles, core_cycles, sleep_cycles),
    "coreExecs": core_execs,
    "util": (lut_util, reg_util, mem_util, dsp_util),
    "power": (dynamic_power, static_power)
  }

  return results
