import subprocess

UNI = True

if UNI:
    XILINX_GNU_PREFIX = "/opt/york/cs/net/xilinx_vivado-2018.2_ise-14.7_x86-64-1/SDK/2018.2/gnu/microblaze/lin/bin/mb-"
else:
    XILINX_GNU_PREFIX = "/tools/Xilinx/SDK/2018.3/gnu/microblaze/lin/bin/mb-"

def run_command(path, flags):
  result = subprocess.run([path] + flags, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return (" ".join(result.args), result.stdout.decode("utf-8"), result.stderr.decode("utf-8"))
