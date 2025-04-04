# %%
import os
import fileUtil
import json5 as json

import nodeWriter

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

# %% Generate contents (index.html, redirect.html)
nodeContent = {}

for nodePath in nodeList:
    nodeMetadata = getNodeMetadata(nodePath)
    if not nodeMetadata:
        print(f"Node data for {nodePath} not found.")
        continue
    
    nodeBase = nodeMetadata["baseNode"]
    nodeName = nodeMetadata["name"]
    
    contentPath = f"../content/__nodes/{fileUtil.pathSanitize(nodeName)}.html"
    fileUtil.verifyFile(contentPath)

    content = nodeWriter.writeNode(nodeMetadata, contentPath)
    if not content:
        print(f"Node content for {nodeBase} not found.")
        continue

    nodeContent[nodeBase] = content
    
# %% Write content to file using category
targetRoot = "../pregen/3_nodes"
fileUtil.verifyFile("../docs/nodes/_index/index.html", f'''<!DOCTYPE html><html></html>''')
fileUtil.verifyFolder(targetRoot)

nodeCategoryDir = "D:/Project/MakhamDev/LTS-PixelComposer/PixelComposer/datafiles/data/Nodes/display_data.json"
with open(nodeCategoryDir, 'r') as f:
    nodeCategoryData = json.load(f)

nodeCategory = {}
for category in nodeCategoryData:
    name  = category["name"]
    nodes = category["nodes"]
    nodeCategory[name] = nodes
    
    categoryDir = os.path.join(targetRoot, fileUtil.pathSanitize(name))
    fileUtil.verifyFile(f"{categoryDir}/index.html", f'''<!DOCTYPE html><html></html>''')

    for node in nodes:
        if not isinstance(node, str):
            continue

        if node not in nodeContent:
            print(f"Node content for {node} not found.")
            continue

        targetPath = os.path.join(categoryDir, fileUtil.pathSanitize(node) + ".html")
        fileUtil.writeFile(targetPath, nodeContent[node])

    