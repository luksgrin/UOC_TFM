import sys
from functools import reduce

filepath = sys.argv[1]
referencefile = "../../../../data/RMM1.pdb"

with open(filepath) as file:
    contents = file.read()

with open(referencefile) as file:
    structure = str(reduce(
        lambda x,y: (x + y)
        if (y[:5] in ("HELIX", "SHEET")) 
        else x,
        file.readlines(),
        ""
    ))

with open(filepath, "w") as file:
    file.write(structure + contents)