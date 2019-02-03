from . import common

GCC = common.XILINX_GNU_PREFIX + "gcc"

def help():
  common.run_command(GCC, ["--help"])

def compile(files, output):
  common.run_command(GCC, ["-S"] + files + ["-o " + output])

def assemble(files, output):
  common.run_command(GCC, files + ["-o " + output])