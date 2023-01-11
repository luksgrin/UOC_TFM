#!/usr/bin/env python3

# NOTE BY LUCAS (NOVEMBER 2022):
# use this on .pdb files corresponding to RNA structures only!

"""
ATOM     23  H5'  DG B   1     -15.347  -3.940  -5.934  1.00  0.00           H   new
ATOM     24 H5''  DG B   1     -15.852  -4.851  -7.094  1.00  0.00           H   new
ATOM     25  H4'  DG B   1     -15.214  -3.222  -8.238  1.00  0.00           H   new
ATOM     26  H3'  DG B   1     -13.483  -5.075  -8.732  1.00  0.00           H   new
ATOM     27  H2'  DG B   1     -11.785  -4.224  -7.287  1.00  0.00           H   new
ATOM     28 H2''  DG B   1     -11.314  -3.732  -8.690  1.00  0.00           H   new
ATOM     29  H1'  DG B   1     -12.430  -1.717  -8.491  1.00  0.00           H   new
ATOM     30  H8   DG B   1     -10.897  -3.080  -5.447  1.00  0.00           H   new
ATOM     31  H1   DG B   1     -10.070   2.951  -6.160  1.00  0.00           H   new
ATOM     32  H21  DG B   1     -12.087   2.806  -8.716  1.00  0.00           H   new
ATOM     33  H22  DG B   1     -11.235   3.696  -7.879  1.00  0.00           H   new
"""

import os
import argparse
from lightdock.scoring.dna.data.amber import atoms_per_residue
from lightdock.pdbutil.PDBIO import read_atom_line


def _format_atom_name(atom_name):
    """Format ATOM name with correct padding"""
    if len(atom_name) == 4:
        return atom_name
    else:
        return " %s" % atom_name


def write_atom_line(atom, output):
    """Writes a PDB file format line to output."""
    if atom.__class__.__name__ == "HetAtom":
        atom_type = "HETATM"
    else:
        atom_type = "ATOM  "
    line = "%6s%5d %-4s%-1s%3s%2s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f%12s\n" % (
        atom_type,
        atom.number,
        _format_atom_name(atom.name),
        atom.alternative,
        atom.residue_name,
        atom.chain_id,
        atom.residue_number,
        atom.residue_insertion,
        atom.x,
        atom.y,
        atom.z,
        atom.occupancy,
        atom.b_factor,
        atom.element,
    )
    output.write(line)


translation = {
    "H5'": "H5'1",
    "H5''": "H5'2",
    "H2'": "H2'1", 
    "H2''": "H2'2", 
    "HO2'": "HO'2", # These ones were added by Lucas in November 2022
    "HO3'": "HO'3", #
    "HO5'": "HO'5"  #
}


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdb_file")
    parser.add_argument("output_pdb_file")
    args = parser.parse_args()

    with open(args.input_pdb_file) as ih:
        with open(args.output_pdb_file, 'w') as oh:
            for line in ih:
                line = line.rstrip(os.linesep)
                if line.startswith("ATOM  "):
                    atom = read_atom_line(line)

                    # The following lines were added by Lucas in November 2022 #
                    if (                                                       #
                        not(atom.residue_name.startswith("R"))                 #
                        and not(atom.residue_name.startswith("D"))             #
                        ):                                                     #
                        atom.residue_name = "R" + atom.residue_name            #
                    ############################################################
                    if atom.residue_name not in atoms_per_residue:
                        print(f"Not supported atom: {atom.residue_name}.{atom.name}")
                    else:
                        if atom.name not in atoms_per_residue[atom.residue_name] and atom.is_hydrogen():
                            try:
                                atom.name = translation[atom.name]
                                write_atom_line(atom, oh)
                            except KeyError:
                                print(f"Atom not found in mapping: {atom.residue_name}.{atom.name}")
                        else:
                            write_atom_line(atom, oh)

