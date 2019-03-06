#!/usr/bin/python3

import os
import shutil
import getopt
import sys

import matplotlib.pyplot as plot

from testbench import testing

HELP = """Usage: code-to-silicon.py <options>
          Options:
            --nosim:    avoid running Vivado simulations.
            --nosynth:  avoid running synthesis and analysis in Vivado.
            --noreport: avoid building LaTeX reort.
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

  # Logging level WARNING.
  verbosity = Logger.WARNING

  # Initialize a logger with the default level.
  logger = Logger(verbosity)

  # Parse command line arguments.
  try:
    opts, args = getopt.getopt(argv, "h", ["nosim", "nosynth", "noreport", "verbosity=", "help"])
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
    elif opt == "--verbosity":
      verbosity = int(arg)

      if verbosity < 0 or verbosity > 3:
        logger.error("Invalid verbosity level " + str(verbosity))
        sys.exit(2)

  # Set the logger's actual level now that we've parsed the options.
  logger.setLevel(verbosity)

  if os.path.isdir("figures/autogen"):
    shutil.rmtree("figures/autogen")

  os.makedirs("figures/autogen")

  coreCounts = []
  speedups = []
  coreInputsAvg = []
  coreOutputsAvg = []
  baseCycles = None

  cores = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66]

  for i in cores:
    metrics = testing.runTest(logger, "fannkuch", i, sim)

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
      plot.scatter(metrics["coreInputs"], metrics["coreOutputs"])
      plot.xlim([0, 32])
      plot.ylim([0, 32])
      plot.savefig("figures/autogen/pop-{:02d}-cores.png".format(metrics["coreCount"]))
      plot.clf()

      # Plot regression of heuristic cost against actual cost.
      plot.scatter(metrics["heuristicCost"], metrics["actualCost"])
      plot.savefig("figures/autogen/cost-{:02d}-cores.png".format(metrics["coreCount"]))
      plot.clf()

      # Store average inputs and outputs.
      coreInputsAvg.append(sum(metrics["coreInputs"])/len(metrics["coreInputs"]))
      coreOutputsAvg.append(sum(metrics["coreOutputs"])/len(metrics["coreOutputs"]))

  # Display a plot of speedup against core count.
  if sim:
    plot.plot(coreCounts, speedups)
    plot.savefig("figures/autogen/speedup-sha256.png")
    plot.clf()

  # Plot average inputs/outputs against core count.
  plot.plot(coreCounts, coreInputsAvg)
  plot.plot(coreCounts, coreOutputsAvg)
  plot.xlim([1, coreCounts[-1]])
  plot.ylim([0, 32])
  plot.savefig("figures/autogen/avg-outputs.png")
  plot.clf()

  # Now build the report (unless we've been asked not to)!
  if report:
    os.system("pdflatex REPORT > texbuild.log")
    os.system("biber REPORT > texbuild.log")
    os.system("pdflatex REPORT > texbuild.log")

  # The Vivado project will have been modified. Revert it.
  os.system("git checkout microblaze_system/microblaze_system.xpr")

if __name__ == "__main__":
  main(sys.argv[1:])
