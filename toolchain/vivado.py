from . import common

VIVADO = "vivado"

def start_tcl():
    common.run_command(VIVADO, ["-mode tcl"])

def start_batch(script):
    common.run_command(VIVADO, ["-mode batch", "-source " + script])
