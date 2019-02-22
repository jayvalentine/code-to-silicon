import os
import shutil

import templating
from toolchain import compiler, memory, vivado

TESTING_DIR = os.path.abspath("testbench")
TEMPLATE_DIR = os.path.abspath("templates")

def runTest(testName):
    # Get test and temp directory paths.
    testDir = os.path.join(TESTING_DIR, testName)
    tempDir = os.path.join(testDir, "temp")

    # If the temp directory already exists, delete it.
    if os.path.isdir(tempDir):
        shutil.rmtree(tempDir)

    os.makedirs(tempDir)

    # Copy everything in the test dir into the temp dir.
    files = [f for f in os.listdir(testDir) if os.path.isfile(os.path.join(testDir, f))]

    for file in files:
        print(file)
        shutil.copy(os.path.join(testDir, file), tempDir)

    # Move to the temp directory.
    origDir = os.getcwd()
    os.chdir(tempDir)

    # Compile files.
    compileApplication()
    writeMemoryInitFile()
    generateTemplates()
    runVivado()

    # Move back to the root directory.
    os.chdir(origDir)

def compileApplication():
    compiler.compile(["application.c"], "application.s")

    # Compile the harness and test functions.
    compiler.compile(["main.c"], "main.s")
    compiler.compile(["test.c"], "test.s")

    # Link the assembly file with start.s, and make a hex file.
    # Disassemble this file for later reference.
    compiler.link(["application.s", "test.s", "main.s", "start.s"], "main.elf")
    compiler.makeHex("main.elf", "main.hex")
    compiler.disassembleElf("main.elf", "main.asm")

def writeMemoryInitFile():
    # Generate a memory initialization file ('memory.txt') from the hex file.
    memory.writeMemoryFile("memory.txt", "main.hex")

def generateTemplates():
    # Read the ELF symbols.
    syms = compiler.getElfSymbols("main.elf")

    vars_testbench = {
        "FAILED_ADDR": syms["test_failed"],
        "PASSED_ADDR": syms["test_passed"]
    }

    # Generate testbench template.
    tbTemplate = os.path.join(TEMPLATE_DIR, "testbench.vhd")
    tclTemplate = os.path.join(TEMPLATE_DIR, "simulate.tcl")

    templating.processTemplate(tbTemplate, "testbench.vhd", vars_testbench)
    templating.processTemplate(tclTemplate, "simulate.tcl", {})

def runVivado():
    print(vivado.start_batch("simulate.tcl"))
