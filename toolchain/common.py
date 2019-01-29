import os

# Lets just assume that the Xilinx Microblaze GNU tools are on our PATH.
XILINX_GNU_PREFIX = "microblazeel-xilinx-linux-gnu-"

def run_command(path, flags):
  cmd = path + " " + " ".join(flags)
  print(cmd)
  os.system(cmd)