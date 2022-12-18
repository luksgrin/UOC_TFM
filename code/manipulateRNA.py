import sys

def reemplazar(line):
    line = list(line)
    line[line.index("R")] = " "
    return "".join(line)

with open(sys.argv[1]) as file:
    lines = file.readlines()


S = list(map(
    reemplazar,
    lines
))

with open(sys.argv[1], "w") as file:
    file.write("".join(S))