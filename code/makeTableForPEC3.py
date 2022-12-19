import pandas as pd
from read_solutionslist import parseResultsList

querypath = "./dockings/{}/no_restraints/solutions.list"

subjects = (
    "RMM1_orig",
    "RMM1_mut1",
    "RMM1_mut2",
    "RMM1_mut3",
    "RMM1_mut4",
    "RMM1_mut5",
)

dfs = []

for ddir in subjects:

    dfs.append(
        parseResultsList(
            querypath
            .format(ddir)
        )
        .head(n=10)
        .reset_index(drop=True)
        [["Luciferin", "Scoring"]]
    )

print(pd.concat(dfs, keys=subjects))