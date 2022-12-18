import sys, os
from read_solutionslist import parseResultsList

solutionsFilePath = sys.argv[1]
parentPath = "."

if solutionsFilePath.find("/") != -1:
    parentPath += ("/" + "/".join(solutionsFilePath.split("/")[:-1]))

df = parseResultsList(solutionsFilePath).head(n=10).reset_index(drop=True)


finalResultsPath = parentPath + "/winners"

os.mkdir(finalResultsPath)


winners = df.apply(
    lambda row: (
        parentPath
        + "/swarm_%s/%s"
        % (row["Swarm"], row["PDB"])
    ),
    axis=1
).reset_index()


winners.apply(
    lambda row: os.rename(
        row[0],
        (
            finalResultsPath
            + "/%s_"
            + row[0].split("/")[-1]
        ) % row["index"]
    ),
    axis=1
)