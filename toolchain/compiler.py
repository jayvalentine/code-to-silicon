import re

from . import common

GCC = common.XILINX_GNU_PREFIX + "gcc"
OBJCOPY = common.XILINX_GNU_PREFIX + "objcopy"
OBJDUMP = common.XILINX_GNU_PREFIX + "objdump"
READELF = common.XILINX_GNU_PREFIX + "readelf"

SYM_FORMAT = re.compile("\s*\d+: ([0-9a-f]{8})\s+\d+ \w+\s+\w+\s+\w+\s+\S+ (\w+)")

def help():
  common.run_command(GCC, ["--help"])

def compile(files, output):
  common.run_command(GCC, ["-S", "-Xassembler", "-ahlsm", "-mno-xl-soft-div", "-mhard-float", "-mno-xl-soft-mul", "-fno-delayed-branch", "-flive-range-shrinkage", "-funroll-all-loops", "-Os"] + ["-o " + output] + files)

def link(files, output):
  common.run_command(GCC, ["-Wl,-Tlink.x,-Map=link.map", "-nostartfiles"] + ["-o " + output] + files)

def makeHex(objfile, hexfile):
  common.run_command(OBJCOPY, ["-O", "ihex", objfile, hexfile])

def disassembleElf(elffile, asmfile):
  return common.run_command(OBJDUMP, ["-d", elffile])

def getElfSymbols(elffile):
  out = common.run_command(READELF, ["-s", elffile])

  syms = {}

  for line in out.splitlines():
      # See if the line matches our regex.
      print(line)
      m = SYM_FORMAT.match(line)
      if m != None:
          syms[m.groups()[1]] = m.groups()[0]

  return syms
