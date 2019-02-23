import subprocess

# Lets just assume that the Xilinx Microblaze GNU tools are on our PATH.
XILINX_GNU_PREFIX = "microblazeel-xilinx-linux-gnu-"

def run_command(path, flags):
  result = subprocess.run([path] + flags, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return (" ".join(result.args), result.stdout.decode("utf-8"), result.stderr.decode("utf-8"))
