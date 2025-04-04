# %% 
import os
import re

import juncParser

scriptDir   = "D:/Project/MakhamDev/LTS-PixelComposer/PixelComposer/scripts"
nodeScripts = {}
nodeLists   = []
nodeData    = {}

# %%
def reFindFirst(pattern, string):
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    return ""

#%%
def readNodeScripts():
    scripts = {}

    for _dir in os.listdir(scriptDir):
        if not os.path.isdir(os.path.join(scriptDir, _dir)):
            continue
        
        if not _dir.strip("_").startswith("node_"):
            continue
        
        scriptFile = f"{scriptDir}/{_dir}/{_dir}.gml"
        if not os.path.exists(scriptFile):
            continue

        with open(scriptFile, "r") as f:
            script = f.read()
        
        baseNode = reFindFirst(r"function\s(\w*)\(.*constructor", script).strip()
        if not baseNode:
            continue
        if not baseNode.strip("_").lower().startswith("node_"):
            continue

        scripts[baseNode] = script

    return scripts

nodeScripts = readNodeScripts()
nodeLists   = list(nodeScripts.keys())

# %%
def readNodeFile(baseNode):
    if baseNode not in nodeScripts:
        print(f"Node script for {baseNode} not found.")
        return None
    
    script = nodeScripts[baseNode]
    
    classParent = reFindFirst(r"function.*:\s(\w*)", script).strip()

    inputs = re.findall(r"^\s*newInput.*$", script, re.MULTILINE)
    inputs = juncParser.parseInputs(inputs)

    outputs = re.findall(r"^\s*newOutput.*$", script, re.MULTILINE)
    outputs = juncParser.parseOutputs(outputs)

    data = {
        "name":        baseNode,
        "classParent": classParent,
        "inheritances":[],

        "inputs":      inputs,
        "outputs":     outputs,
        "categories":  [],
        "attributes":  [],
    }

    return data

for baseNode in nodeLists:
    nodeData[baseNode] = readNodeFile(baseNode)

# %% 
def inheritancesIterate(baseNode):
    if baseNode not in nodeData:
        print(f"Node data for {baseNode} not found.")
        return None
    
    print(f"Iterating parents for {baseNode}")
    inheritances = [nodeData[baseNode]]
    currentNode  = baseNode

    while True:
        data    = nodeData[currentNode]
        cparent = data["classParent"]

        if cparent == "" or cparent not in nodeData:
            break

        inheritances.insert(0, nodeData[cparent])

        if data["classParent"] == "node":
            break
        
        currentNode = data["classParent"]
    
    nodeData[baseNode]["inheritances"] = inheritances

for baseNode in nodeLists:
    inheritancesIterate(baseNode)

# %%
def getNodeData(baseNode):
    if baseNode not in nodeData:
        print(f"Node data for {baseNode} not found.")
        return None
    
    return nodeData[baseNode]

