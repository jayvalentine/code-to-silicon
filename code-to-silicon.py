#!/usr/bin/python3

import os
import shutil
import getopt
import sys

import matplotlib.pyplot as plot
import matplotlib.patches as patches

from testbench import testing

HELP = """Usage: code-to-silicon.py <options>
          Options:
            --nosim:           avoid running Vivado simulations.
            --nosynth:         avoid running synthesis and analysis in Vivado.
            --noreport:        avoid building LaTeX reort.
            --nofig:           avoid generating figures.
            --verbosity=level  logging level.
            --analysis=mode    analysis complexity.
            --pruning=mode     block output pruning mode.
            --help, -h: display this message."""

class Logger:
  DEBUG = 0
  INFO = 1
  WARNING = 2
  ERROR = 3

  def __init__(self, level):
    self._level = level

  def _level(level):
    if level == Logger.DEBUG:
      return "DEBUG"
    elif level == Logger.INFO:
      return "INFO"
    elif level == Logger.WARNING:
      return "WARNING"
    elif level == Logger.ERROR:
      return "ERROR"
    else:
      raise ValueError("Invalid log level: " + str(level))

  def _send(self, message, level):
    if level >= self._level:
      print(Logger._level(level) + ": " + str(message))

  def debug(self, message):
    self._send(message, Logger.DEBUG)

  def info(self, message):
    self._send(message, Logger.INFO)

  def warn(self, message):
    self._send(message, Logger.WARNING)

  def error(self, message):
    self._send(message, Logger.ERROR)

  def setLevel(self, level):
    self._level = level

def main(argv):
  # Ensure the vivado project is clean when we start.
  os.system("git checkout microblaze_system/microblaze_system.xpr")

  sim = True
  report = True
  fig = True

  pruningModes = ["naive", "volatile", "dependency"]
  selectionModes = ["hybrid", "avgwidth", "size"]

  tests = ["fannkuch", "sha256", "fft", "sum_squares"]

  # Logging level WARNING.
  verbosity = Logger.WARNING

  # Initialize a logger with the default level.
  logger = Logger(verbosity)

  # Parse command line arguments.
  try:
    opts, args = getopt.getopt(argv, "h", ["nosim", "nosynth", "noreport", "nofig", "verbosity=", "selection=", "pruning=", "tests=", "help"])
  except getopt.GetoptError:
    print(HELP)
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print(HELP)
      sys.exit()
    elif opt == "--nosim":
      sim = False
    elif opt == "--noreport":
      report = False
    elif opt == "--nosynth":
      logger.warn("Unimplemented option --nosynth.")
    elif opt == "--nofig":
      fig = False
    elif opt == "--verbosity":
      verbosity = int(arg)

      if verbosity < 0 or verbosity > 3:
        logger.error("Invalid verbosity level " + str(verbosity))
        sys.exit(2)
    elif opt == "--selection":
      modesNew = str(arg).split(",")
      for m in modesNew:
        if m not in selectionModes:
          logger.error("Invalid selection mode '" + m + "'.")
          sys.exit(2)

      selectionModes = modesNew

    elif opt == "--pruning":
      modesNew = str(arg).split(",")
      for m in modesNew:
        if m not in pruningModes:
          logger.error("Invalid pruning mode '" + m + "'.")
          sys.exit(2)

      pruningModes = modesNew

    elif opt == "--tests":
      testsNew = str(arg).split(",")
      for t in testsNew:
        if t not in tests:
          logger.error("Invalid test '" + t + "'.")
          sys.exit(2)

      tests = testsNew

  # Set the logger's actual level now that we've parsed the options.
  logger.setLevel(verbosity)

  if os.path.isdir("figures/autogen"):
    shutil.rmtree("figures/autogen")

  os.makedirs("figures/autogen")

  cores = [0, 1, 2, 3, 4, 6, 8, 10, 15, 21, 28, 36, 45]

  outputLines = []

  with open("results.csv", 'w+') as results:
    results.write("testname,analysistype,pruningmode,result,cores,cycles,analysistime\n")

  for testName in tests:
    analysisTimes = {}
    speedups = {}
    for selection in selectionModes:
      for pruning in pruningModes:
        coreCounts = []
        coreInputsAvg = []
        coreOutputsAvg = []
        baseCycles = None
        cycleBreakdowns = []

        i = 0
        done = False
        while i < len(cores) and not done:
          metrics = testing.runTest(logger, testName, cores[i], sim, selection, pruning)

          cycleBreakdowns.append(metrics["cycleBreakdown"])

          # Set the 'done' flag if the system produces fewer cores than we told it to.
          # this indicates that we've reached saturation.
          if metrics["coreCount"] < cores[i]:
            done = True

          if metrics["result"] == None:
            result = "not-run"
          elif metrics["result"]:
            result = "passed"
          else:
              result = "failed"

          if selection not in analysisTimes.keys():
            analysisTimes[selection] = {}

          if pruning not in analysisTimes[selection].keys():
            analysisTimes[selection][pruning] = []

          if selection not in speedups.keys():
            speedups[selection] = {}

          if pruning not in speedups[selection].keys():
            speedups[selection][pruning] = []

          analysisTimes[selection][pruning].append(metrics["analysisTime"])

          if cores[i] == 0:
            speedups[selection][pruning].append(1.0)
            coreCounts.append(0)
            baseCycles = metrics["cycles"]
            coreInputsAvg.append(0)
            coreOutputsAvg.append(0)

            inputs = metrics["blockInputs"]
            outputs = metrics["blockOutputs"]
            sizes = metrics["blockSize"]
            memDensities = metrics["blockMemDensity"]

            if fig:
              plot.hist(inputs, 32)
              plot.xlabel("# of input registers")
              plot.ylabel("Occurances")
              plot.savefig("figures/autogen/block-inputs-{:s}.png".format(testName))
              plot.clf()

              plot.hist(outputs, 32)
              plot.xlabel("# of output registers")
              plot.ylabel("Occurances")
              plot.savefig("figures/autogen/block-outputs-{:s}.png".format(testName))
              plot.clf()

              plot.hist(sizes, 10)
              plot.xlabel("Block size (# of instructions)")
              plot.ylabel("Occurances")
              plot.savefig("figures/autogen/block-sizes-{:s}.png".format(testName))
              plot.clf()

              plot.hist(memDensities, 10)
              plot.xlabel("Block memory access density")
              plot.ylabel("Occurances")
              plot.savefig("figures/autogen/block-mem-densities-{:s}.png".format(testName))
              plot.clf()

          else:
            if metrics["cycles"] != None:
              s = baseCycles / metrics["cycles"]
              speedups[selection][pruning].append(s)

            coreCounts.append(metrics["coreCount"])

            # Plot 'population scatter' of inputs vs outputs.
            if fig:
              plot.scatter(metrics["coreInputs"], metrics["coreOutputs"])
              plot.xlim([0, 32])
              plot.ylim([0, 32])

              plot.xlabel("# of input registers")
              plot.ylabel("# of output registers")

              plot.savefig("figures/autogen/pop-{:s}-{:02d}-cores-{:s}.png".format(testName, metrics["coreCount"], selection + "-" + pruning))
              plot.clf()

              # Plot regression of heuristic cost against actual cost.
              plot.scatter(metrics["heuristicCost"], metrics["actualCost"])

              plot.xlabel("Estimated cost")
              plot.ylabel("Actual IPC (instructions per clock)")

              plot.savefig("figures/autogen/cost-{:s}-{:02d}-cores-{:s}.png".format(testName, metrics["coreCount"], selection + "-" + pruning))
              plot.clf()

            # Store average inputs and outputs.
            coreInputsAvg.append(sum(metrics["coreInputs"])/len(metrics["coreInputs"]))
            coreOutputsAvg.append(sum(metrics["coreOutputs"])/len(metrics["coreOutputs"]))

          with open("results.csv", 'a') as results:
            results.write(",".join([testName, selection, pruning, result, str(metrics["coreCount"]), str(metrics["cycles"]), str(round(metrics["analysisTime"], 4))]) + "\n")

          i += 1

        # Plot average inputs/outputs against core count.
        if fig:
          plot.plot(coreCounts, coreInputsAvg, label="Input")
          plot.plot(coreCounts, coreOutputsAvg, label="Output")
          plot.legend(loc = "upper left")
          plot.xlim([1, coreCounts[-1]])
          plot.ylim([0, 32])

          plot.xlabel("Core count")
          plot.ylabel("Register count")

          plot.savefig("figures/autogen/avg-io-{:s}-{:s}.png".format(testName, selection + "-" + pruning))
          plot.clf()

          # Display a plot of speedup against core count.
          if sim:
            mb_bd = []
            axi_bd = []
            core_bd = []
            sleep_bd = []

            for bd in cycleBreakdowns:
              mb_bd.append(bd[0])
              axi_bd.append(bd[0] + bd[1])
              core_bd.append(bd[0] + bd[1] + bd[2])
              sleep_bd.append(bd[0] + bd[1] + bd[2] + bd[3])

            plot.plot(coreCounts, mb_bd, label="microblaze", color="black")
            plot.plot(coreCounts, axi_bd, label="axi transfer", color="black")
            plot.plot(coreCounts, core_bd, label="accelerator cores", color="black")
            plot.plot(coreCounts, sleep_bd, label="sleep overhead", color="black")
            plot.fill_between(coreCounts, [0 for i in range(len(coreCounts))], mb_bd, color="orange")
            plot.fill_between(coreCounts, mb_bd, axi_bd, color="blue")
            plot.fill_between(coreCounts, axi_bd, core_bd, color="green")
            plot.fill_between(coreCounts, core_bd, sleep_bd, color='red')

            orange_patch = patches.Patch(color='orange', label='MicroBlaze')
            blue_patch = patches.Patch(color='blue', label='AXI transfer')
            green_patch = patches.Patch(color='green', label='Accelerator cores')
            red_patch = patches.Patch(color='red', label='Sleep overhead')
            plot.legend(handles=[orange_patch, blue_patch, green_patch, red_patch], loc="upper left")

            plot.xlabel("Core count")
            plot.ylabel("Clock cycles")

            plot.savefig("figures/autogen/cycles-breakdown-{:s}-{:s}.png".format(testName, selection + "-" + pruning))
            plot.clf()

    # Plot analysis times against core count.
    if fig:
      for selection in selectionModes:
        for mode in pruningModes:
          plot.plot(coreCounts, analysisTimes[selection][mode], label=selection + ", " + mode)

      plot.legend(loc="upper left")
      plot.xlim([0, coreCounts[-1]])

      plot.xlabel("Core count")
      plot.ylabel("Analysis time (seconds)")

      plot.savefig("figures/autogen/analysis-times-{:s}.png".format(testName))
      plot.clf()

      # Display a plot of speedup against core count.
      if sim:
        for selection in selectionModes:
          for pruning in pruningModes:
            plot.plot(coreCounts, speedups[selection][pruning], label=selection + ", " + pruning)

        plot.plot(coreCounts, [1.0 for i in range(len(coreCounts))], 'r--', label="baseline")
        plot.legend(loc="upper right")

        plot.xlabel("Core count")
        plot.ylabel("Speedup")

        plot.savefig("figures/autogen/speedup-{:s}.png".format(testName))
        plot.clf()

  # Now build the report (unless we've been asked not to)!
  if report:
    os.system("pdflatex REPORT > texbuild.log")
    os.system("biber REPORT > texbuild.log")
    os.system("pdflatex REPORT > texbuild.log")

if __name__ == "__main__":
  main(sys.argv[1:])
