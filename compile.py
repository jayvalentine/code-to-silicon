import os

# Lets just assume that the Xilinx Microblaze GNU tools are on our PATH.
XILINX_GNU_PREFIX = "microblazeel-xilinx-linux-gnu-"

GCC = XILINX_GNU_PREFIX + "gcc"

def run_command(path, flags):
  cmd = path + " " + " ".join(flags)
  print(cmd)
  os.system(cmd)

def gcc_help():
  run_command(GCC, ["--help"])