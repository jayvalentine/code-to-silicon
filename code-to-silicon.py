#!/usr/bin/python3

import os
import shutil
import getopt
import sys

import matplotlib.pyplot as plot

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
  sim = True
  report = True
  fig = True

  # Logging level WARNING.
  verbosity = Logger.WARNING

  # Initialize a logger with the default level.
  logger = Logger(verbosity)

  # Parse command line arguments.
  try:
    opts, args = getopt.getopt(argv, "h", ["nosim", "nosynth", "noreport", "nofig", "verbosity=", "analysis=", "pruning=", "help"])
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
    elif opt == "--analysis":
      analysis = str(arg)
      if analysis not in ["heuristic", "expensive", "both"]:
        logger.error("Invalid analysis mode " + analysis)
        sys.exit(2)

      analysisTypes = ["heuristic", "expensive"]
      if analysis == "heuristic":
        analysisTypes = ["heuristic"]
      elif analysis == "expensive":
        analysisTypes = ["expensive"]

    elif opt == "--pruning":
      mode = str(arg)
      if mode not in ["naive", "volatile", "complete"]:
        logger.error("Invalid pruning mode " + mode)
        sys.exit(2)

  # Set the logger's actual level now that we've parsed the options.
  logger.setLevel(verbosity)

  if os.path.isdir("figures/autogen"):
    shutil.rmtree("figures/autogen")

  os.makedirs("figures/autogen")

  cores = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66]

  analysisTimes = {}

  outputLines = []

  testName = "fannkuch"

  for analysis in analysisTypes:
    coreCounts = []
    speedups = []
    coreInputsAvg = []
    coreOutputsAvg = []
    baseCycles = None

    for i in cores:
      metrics = testing.runTest(logger, testName, i, sim, analysis, mode)

      if analysis not in analysisTimes.keys():
        analysisTimes[analysis] = []

      analysisTimes[analysis].append(metrics["analysisTime"])

      if i == 0:
        speedups.append(1.0)
        coreCounts.append(0)
        baseCycles = metrics["cycles"]
        coreInputsAvg.append(0)
        coreOutputsAvg.append(0)

      else:
        if metrics["cycles"] != None:
          s = baseCycles / metrics["cycles"]
          speedups.append(s)

        coreCounts.append(metrics["coreCount"])

        # Plot 'population scatter' of inputs vs outputs.
        if fig:
          plot.scatter(metrics["coreInputs"], metrics["coreOutputs"])
          plot.xlim([0, 32])
          plot.ylim([0, 32])
          plot.savefig("figures/autogen/pop-{:02d}-cores-{:s}.png".format(metrics["coreCount"], analysis))
          plot.clf()

          # Plot regression of heuristic cost against actual cost.
          plot.scatter(metrics["heuristicCost"], metrics["actualCost"])
          plot.savefig("figures/autogen/cost-{:02d}-cores-{:s}.png".format(metrics["coreCount"], analysis))
          plot.clf()

        # Store average inputs and outputs.
        coreInputsAvg.append(sum(metrics["coreInputs"])/len(metrics["coreInputs"]))
        coreOutputsAvg.append(sum(metrics["coreOutputs"])/len(metrics["coreOutputs"]))

      outputLines.append(",".join([testName, analysis, mode, str(metrics["coreCount"]), str(metrics["cycles"]), str(round(metrics["analysisTime"], 4))]))

    # Display a plot of speedup against core count.
    if sim and fig:
      plot.plot(coreCounts, speedups)
      plot.savefig("figures/autogen/speedup-fannkuch-{:s}.png".format(analysis))
      plot.clf()

    # Plot average inputs/outputs against core count.
    if fig:
      plot.plot(coreCounts, coreInputsAvg, label="Input")
      plot.plot(coreCounts, coreOutputsAvg, label="Output")
      plot.legend(loc = "upper left")
      plot.xlim([1, coreCounts[-1]])
      plot.ylim([0, 32])
      plot.savefig("figures/autogen/avg-io-{:s}.png".format(analysis))
      plot.clf()

  # Plot analysis times against core count.
  if fig:
    for analysis in analysisTypes:
      plot.plot(coreCounts, analysisTimes[analysis], label=analysis)

    plot.legend(loc="upper left")
    plot.xlim([0, coreCounts[-1]])
    plot.savefig("figures/autogen/analysis-times.png")
    plot.clf()

  with open("results.csv", 'w') as csv:
    for l in outputLines:
      csv.write(l + "\n")

  # Now build the report (unless we've been asked not to)!
  if report:
    os.system("pdflatex REPORT > texbuild.log")
    os.system("biber REPORT > texbuild.log")
    os.system("pdflatex REPORT > texbuild.log")

  # The Vivado project will have been modified. Revert it.
  os.system("git checkout microblaze_system/microblaze_system.xpr")

if __name__ == "__main__":
  main(sys.argv[1:])
