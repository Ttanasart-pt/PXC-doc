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
    iType = reFindFirst(r"^.*nodeValue(.*?)\(", inp).strip(" _")
    iName = reFindFirst(r'"(.*?)"', inp)

    return {
        "name": iName,
        "type": iType, 
    }

def parseInputs(inputs):
    return [parseInput(i) for i in inputs]
# %%

def parseOutput(out):
    out   = out.strip()
    oType = reFindFirst(r"^.*VALUE_TYPE\.(.*?)\,", out).strip(" _")
    oName = reFindFirst(r'"(.*?)"', out)

    return {
        "name": oName,
        "type": oType, 
    }

def parseOutputs(outputs):
    return [parseOutput(o) for o in outputs]
# %%
