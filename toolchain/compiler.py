from . import common

GCC = common.XILINX_GNU_PREFIX + "gcc"

def help():
  common.run_command(GCC, ["--help"])

def compile(files, output):
  common.run_command(GCC, ["-S -Xassembler -ahlsm -mno-xl-soft-div -mhard-float -mno-xl-soft-mul -nostartfiles -fno-delayed-branch -flive-range-shrinkage -funroll-all-loops -Os"] + files + ["-o " + output])

def assemble(files, output):
  common.run_command(GCC, files + ["-o " + output])