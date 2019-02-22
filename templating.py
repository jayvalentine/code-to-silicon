def token(name):
    return "%%" + name + "%%"

def processTemplate(templateFile, destination, values):
    # Read in the template file.
    with open(templateFile, 'r') as f:
        template = f.read()

    # Process all the values.
    out = template
    for var in values.keys():
        # Replace the token with the value.
        out = out.replace(token(var), values[var])

    with open(destination, 'w') as f:
        f.write(out)
