# %%
import os
import fileUtil
import json5 as json

import nodeWriter

# %%  Read node category metadata
nodeCategoryDir = "D:/Project/MakhamDev/LTS-PixelComposer/PixelComposer/datafiles/data/Nodes/display_data.json"
with open(nodeCategoryDir, 'r') as f:
    nodeCategoryData = json.load(f)

# %% Read node metadata
nodeDir  = "D:/Project/MakhamDev/LTS-PixelComposer/PixelComposer/datafiles/data/Nodes/Internal"
nodeList = []
for root, dirs, files in os.walk(nodeDir):
    for file in files:
        if file.endswith(".json"):
            nodeList.append(os.path.join(root, file))

# %% Load node metadata
def getNodeMetadata(nodePath):
    with open(nodePath, 'r') as f:
        nodeData = json.load(f)
    return nodeData

# %% Generate base files (index.html, redirect.html)
nodeMap   = {}
targerDir = "../pregen/3_nodes"

fileUtil.verifyFile("../docs/nodes/_index/index.html", f'''<!DOCTYPE html><html></html>''')
fileUtil.verifyFolder(targerDir)

for nodePath in nodeList:
    nodeMetadata = getNodeMetadata(nodePath)
    
    nodeBase = nodeMetadata["baseNode"]
    nodeName = nodeMetadata["name"]
    nodeMap[nodeName] = nodeBase
    
    contentPath = f"../content/__nodes/{fileUtil.pathSanitize(nodeName)}.html"
    fileUtil.verifyFile(contentPath)

    targetPath  = os.path.join(targerDir, fileUtil.pathSanitize(nodeBase) + ".html")

    nodeWriter.writeNode(nodeMetadata, contentPath, targetPath)

# %%
