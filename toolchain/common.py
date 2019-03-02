import subprocess

# Lets just assume that the Xilinx Microblaze GNU tools are on our PATH.
XILINX_GNU_PREFIX = "/tools/Xilinx/SDK/2018.3/gnu/microblaze/lin/bin/mb-"

def run_command(path, flags):
  result = subprocess.run([path] + flags, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return (" ".join(result.args), result.stdout.decode("utf-8"), result.stderr.decode("utf-8"))
