import re

from . import common

GCC = common.XILINX_GNU_PREFIX + "gcc"
OBJCOPY = common.XILINX_GNU_PREFIX + "objcopy"
OBJDUMP = common.XILINX_GNU_PREFIX + "objdump"
READELF = common.XILINX_GNU_PREFIX + "readelf"

SYM_FORMAT = re.compile("\s*\d+: ([0-9a-f]{8})\s+\d+ \w+\s+\w+\s+\w+\s+\S+ (\w+)")

def help():
  out = common.run_command(GCC, ["--help"])
  logger.debug("GCC: " + out[0])

def compile(logger, files, output):
  out = common.run_command(GCC, ["-S", "-Xassembler", "-ahlsm", "-mno-xl-soft-div", "-mhard-float", "-mxl-soft-mul", "-fno-delayed-branch", "-flive-range-shrinkage", "-ffixed-13", "-ffixed-31", "-O2"] + ["-o", output] + files)
  logger.debug("GCC: " + out[0])

def link(logger, files, output):
  out = common.run_command(GCC, ["-Wl,-T../../link.x,-Map=link.map", "-nostartfiles", "-mlittle-endian"] + ["-o", output] + files)
  logger.debug("GCC: " + out[0])

def makeHex(logger, objfile, hexfile):
  out = common.run_command(OBJCOPY, ["-O", "ihex", objfile, hexfile])
  logger.debug("OBJCOPY: " + out[0])

def disassembleElf(logger, elffile, asmfile):
  out = common.run_command(OBJDUMP, ["-S", "-d", elffile])

  with open(asmfile, 'w') as file:
    file.write(out[1])

  logger.debug("OBJDUMP: " + out[0])


def getElfSymbols(logger, elffile):
  # Get stdout from readelf.
  out = common.run_command(READELF, ["-s", elffile])

  logger.debug("READELF: " + out[0])

  symtab = out[1]

  syms = {}

  for line in symtab.splitlines():
      # See if the line matches our regex.
      m = SYM_FORMAT.match(line)
      if m != None:
          syms[m.groups()[1]] = m.groups()[0]

  return syms
