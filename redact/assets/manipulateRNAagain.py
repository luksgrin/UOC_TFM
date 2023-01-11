import sys

with open(sys.argv[1]) as file:

    filelines = file.readlines()


nufilelines = list(map(
    lambda line: (
        line
        .replace("   A A", "  RA A")
        .replace("   U A", "  RU A")
        .replace("   G A", "  RG A")
        .replace("   C A", "  RC A")
        .replace("   A B", "  RA B")
        .replace("   U B", "  RU B")
        .replace("   G B", "  RG B")
        .replace("   C B", "  RC B")
    ),
    filelines
))

with open(sys.argv[1], "w") as file:
    file.write("".join(nufilelines))