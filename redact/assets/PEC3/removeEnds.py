import sys

with open(sys.argv[1]) as file:
    filelines = filter(
        lambda line: (
            (line.find("HO5'") < 0)
            and (line.find("HO3'") < 0)
        ),
        file.readlines()
    )

print("".join(filelines))