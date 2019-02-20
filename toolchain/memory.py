# Writes a memory initialization file in Xilinx COE format.
def writeMemoryFile(initFileName, hexFileName):
    with open(initFileName, 'w') as initFile:
        with open(hexFileName, 'r') as hexFile:
            for line in hexFile.readlines():
                for mem_line in parseHexLine(line):
                    initFile.write(mem_line)

# Converts a single hex line to a list of memory-init-file lines.
# If this line is an EOF line, returns an empty list.
def parseHexLine(line):
    # We expect the first character to ALWAYS be a colon.
    # Throw an error if this is not the case.
    if line[0] != ':':
        raise ValueError("Invalid hex record: " + line)

    # Get the byte count. This is given in the first 2 characters
    # after the colon.
    byte_count = int(line[1:3], 16)

    # Get the address. This is given in characters 3-6.
    address = int(line[3:7], 16)

    type = int(line[7:9], 16)

    mem_lines = []

    # Type 0 is data.
    if type == 0:

        current_address = address
        for i in range(byte_count):
            b = int(line[9+(i*2):9+((i+1)*2)], 16)

            mem_lines.append("{:d} {:08b}\n".format(current_address, b))
            current_address += 1
    # Type 1 is EOF.
    elif type == 1:
        pass
    else:
        raise ValueError("Invalid HEX record type: " + str(type))

    return mem_lines
