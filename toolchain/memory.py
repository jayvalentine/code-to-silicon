
# Writes a memory initialization file in Xilinx COE format.
def writeMemoryFile(fileName, words, depth):
    fileLines = []

    fileLines.append("memory_initialization_radix=16;\n")
    fileLines.append("memory_initialization_vector=\n")

    for word in words:
        # Get the hexadecimal representation of the word.
        hex = "{:08x},\n".format(word)
        fileLines.append(hex)
        depth -= 1

    while depth > 1:
        fileLines.append("FFFFFFFF,\n")
        depth -= 1

    fileLines.append("\n")

    with open(fileName, 'w') as file:
        file.writelines(fileLines)
