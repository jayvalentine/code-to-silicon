import os

# Lets just assume that the Xilinx Microblaze GNU tools are on our PATH.
XILINX_GNU_PREFIX = "microblazeel-xilinx-linux-gnu-"

GCC = XILINX_GNU_PREFIX + "gcc"

OBJDUMP = XILINX_GNU_PREFIX + "objdump"

def run_command(path, flags):
  cmd = path + " " + " ".join(flags)
  print(cmd)
  os.system(cmd)

def gcc_help():
  run_command(GCC, ["--help"])

def gcc_compile(files, output):
  run_command(GCC, ["-c"] + files + ["-o " + output])

def gcc_link(files, output):
  run_command(GCC, files + ["-o " + output])

def objdump(file, flags, output):
  run_command(OBJDUMP, [file] + flags + ["> " + output])