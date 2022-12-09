import sys, re
from io import StringIO
import pandas as pd

with open(sys.argv[1]) as file:
    filelines = file.readlines()

result = "".join(map(
    lambda line: "\t".join(filter(
        lambda x: x,
        (
            line.replace(
                pat[0],
                pat[0].replace(" ", "")
            ) if (pat:=re.findall("\((.*?)\)", line)) else line
        ).split(" ")
    )),
    filelines
))

df = pd.read_csv(
    StringIO(result),
    sep="\t"
)

df["Coordinates"] = (
    df["Coordinates"]
    .apply(
        lambda x: tuple(
            float(el)
            for el in x[1:-1].split(",")
        )
    )
)

print(df.sort_values("Scoring", ascending=False).tail(n=10))
