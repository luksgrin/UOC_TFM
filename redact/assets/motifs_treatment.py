import os
import datetime
import Bio.SeqIO
import pandas as pd
import nupack as npk
from hashlib import sha256
from subprocess import Popen, PIPE

# Global vars
modelRNA = npk.Model(
    material="rna95-nupack3",
    ensemble="some-nupack3",
    celsius=37,
    sodium=1.0,
    magnesium=0.0
)

# Functions

def alignment(reference:str, case:str) -> str:

    # Absolutely unique name
    name = (
        sha256(bytes(str(datetime.datetime.now()), "UTF-8")).hexdigest() 
        + ".fasta"
    )

    with open(name, "w") as file:
        file.write(
            f">reference\n{reference}\n>case\n{case}\n"
        )

    process = Popen(
        ["mafft", "--clustalout", name],
        stdout=PIPE, stderr=PIPE
    )

    # Should never fail, so I won't check the stderr
    stdout = process.communicate()[0]

    os.remove(name)

    alignInfo = stdout.decode("UTF-8").split("\n")

    return alignInfo[5][-max(len(reference), len(case)):]

def folding(seq:str) -> str:
    
    mfe_structures = npk.mfe(
        strands=[seq],
        model=modelRNA
    )
    
    return str(mfe_structures[0].structure)

def get_data_RNAcomposer(df:pd.DataFrame) -> None:

    series = df.apply(
        lambda row:
        "\n".join([
            ">" + row["name"],
            row["seq"],
            row["structure"]
        ]),
        axis=1
    )

    for el in series:
        print(el)

    return None


def main():

    # Read sequences into data frame    
    seqs = pd.DataFrame([
        (record.id, str(record.seq))
        for record in
        Bio.SeqIO.parse("../data/motifs.fasta", "fasta")
    ])

    seqs.columns = ("name", "seq")

    seqs["alignment"] = seqs["seq"].apply(
        lambda seq: alignment(seqs.loc[0, "seq"], seq)
    )

    seqs["structure"] = seqs["seq"].apply(
        lambda seq: folding(seq)
    )

    return seqs



if __name__ == "__main__":
    s = main()
    print(s)
