import sys
from lightdock.scoring.dna.data.amber import atoms_per_residue

"""http://ambermd.org/Questions/HIS.html

AMBER Histidine residues

Histidine (HIS in normal pdb files) is really one of three possible residues:
HID: Histidine with hydrogen on the delta nitrogen

HIE: Histidine with hydrogen on the epsilon nitrogen

HIP: Histidine with hydrogens on both nitrogens; this is positively charged.

It is up to the user to inspect the environment of each histidine and identify the type that is appropriate.
"""


hists = {
    k:sorted([atom for atom in v if atom.startswith("H")])
    for k,v in atoms_per_residue.items()
    if k.startswith("HI")
}

content = ""

with open(sys.argv[1]) as file:

    isHis = False
    HisH = []
    histinfo = ""

    for line in file:
        elems = line.split()

        if elems[0] == "ATOM":

            if elems[3] == "HIS":
                
                isHis = True
                histinfo += line

                if elems[-2] == "H":
                    HisH.append(elems[2])

                continue

            elif isHis:
                isHis = False
                key = [k for k,v in hists.items() if v == sorted(HisH)][0]

                content += (
                    histinfo.replace("HIS", key)
                    + line
                )

                HisH = []
                histinfo = ""
                continue

            else:
                content += line
                continue

        content += line

print(content)