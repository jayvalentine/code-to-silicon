from . import common

GCC = common.XILINX_GNU_PREFIX + "gcc"
OBJCOPY = common.XILINX_GNU_PREFIX + "objcopy"
OBJDUMP = common.XILINX_GNU_PREFIX + "objdump"

def help():
  common.run_command(GCC, ["--help"])

def compile(files, output):
  common.run_command(GCC, ["-S -Xassembler -ahlsm -mno-xl-soft-div -mhard-float -mno-xl-soft-mul -fno-delayed-branch -flive-range-shrinkage -funroll-all-loops -Os"] + files + ["-o " + output])

def link(files, output):
  common.run_command(GCC, ["-Wl,'-Tlink.x','-Map=link.map' -nostartfiles"] + files + ["-o " + output])

def makeHex(objfile, hexfile):
  common.run_command(OBJCOPY, ["-O ihex", objfile, hexfile])

def disassembleElf(elffile, asmfile):
  common.run_command(OBJDUMP, ["-d", elffile, "> " + asmfile])
