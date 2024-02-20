import os
import shutil
import re

scriptDir = "D:\\Project\\MakhamDev\\LTS-PixelComposer\\PixelComposer\\scripts"
regPath = scriptDir + "\\node_registry\\node_registry.gml"

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

    fileName = className.replace('Node_', '').lower()

    manFilePath = f"content/_nodes/{fileName}.html"
    if os.path.exists(manFilePath):
        with open(manFilePath, "r") as file:
            txt += file.read()
    else:
        with open(manFilePath, "w") as file:
            file.write("")

    filePath = f"content/nodes/{cat}/{fileName}.html"
    with open(filePath, "w") as file:
        file.write(txt)

for line in nodeListRaw.split("\n"):
    line = line.strip()

    if line.startswith("addNodeCatagory("):
        cat = line.split("\"")[1].lower()
        nodes[cat] = []
    elif line.startswith("addNodeObject("):
        args = line.split(",")[1:]

        nodeClass = args[2].strip().strip("\"")
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