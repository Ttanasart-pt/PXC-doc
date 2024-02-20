import os
import shutil
import re

scriptDir = "D:\\Project\\MakhamDev\\LTS-PixelComposer\\PixelComposer\\scripts"
regPath = scriptDir + "node_registry\\node_registry.gml"

content = ""
with open(regPath, "r") as file:
    content = file.read()

nodeListRaws = content.split("// NODE LIST")
nodeListRaw = nodeListRaws[1]

cat   = ""
nodes = {}

def writeNodeFile(cat, node):
    path = f"{scriptDir}\\{node}\\{node}.gml"

    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    
    with open(path, "r") as file:
        content = file.read()

    nodeName  = node
    className = node

    match = re.search(r"name\s*=\s*['\"](.*)['\"]", content)
    if match:
        nodeName = match.group(1)
    
    txt = f"""<h1>{nodeName}</h1>
<p class="subtitle">{className}</p>"""

    filePath = f"content/nodes/{cat}/{className.replace('Node_', '')}.html"
    
    with open(filePath, "w") as file:
        file.write(txt)

for line in nodeListRaw.split("\n"):
    line = line.strip()

    if line.startswith("addNodeCatagory("):
        cat = line.split("\"")[1]
        nodes[cat] = []
    elif line.startswith("addNodeObject("):
        nodeClass = line.split(",")[3].strip().strip("\"")
        nodes[cat].append(nodeClass)

for cat in nodes:
    catPath = f"content/nodes/{cat}"
    if not os.path.exists(catPath):
        os.makedirs(catPath)

    txt = f"""<h1>{cat}</h1>"""
    filePath = f"content/nodes/{cat}/0_index.html"
    with open(filePath, "w") as file:
        file.write(txt)

    for node in nodes[cat]:
        writeNodeFile(cat, node)