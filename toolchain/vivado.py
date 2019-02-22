from . import common

VIVADO = "vivado"

def start_batch(script):
    return common.run_command(VIVADO, ["-mode", "batch", "-source", script])
