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
    ),
    filelines
))

with open(sys.argv[1], "w") as file:
    file.write("".join(nufilelines))