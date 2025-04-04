# %% 
import os
import re

# %%
def reFindFirst(pattern, string):
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    return ""

def parseInput(inp):
    inp   = inp.strip()
    iName = reFindFirst(r'"(.*?)"', inp)
    iType = reFindFirst(r"^.*nodeValue(.*?)\(", inp).strip(" _").lower()

    if iType == "dimension":
        iName = "dimension"
        iType = "dimension"

    if "enum" in iType:
        iType = "enum"

    return {
        "name": iName,
        "type": iType, 
    }

def parseInputs(inputs):
    return [parseInput(i) for i in inputs]
# %%

def parseOutput(out):
    out   = out.strip()
    oName = reFindFirst(r'"(.*?)"', out)
    oType = reFindFirst(r"^.*VALUE_TYPE\.(.*?)\,", out).strip(" _").lower()

    return {
        "name": oName,
        "type": oType, 
    }

def parseOutputs(outputs):
    return [parseOutput(o) for o in outputs]
# %%
