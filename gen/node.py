import os
import shutil
import re
from tqdm import tqdm

import junc

scriptDir = "D:\\Project\\MakhamDev\\LTS-PixelComposer\\PixelComposer\\scripts"
regPath   = scriptDir + "\\node_registry\\node_registry.gml"
dirname   = "3_nodes"

templatePath = "templates/node.html"
with open(templatePath, "r") as f:
    template = f.read()

content = ""
with open(regPath, "r") as file:
    content = file.read()

nodeListRaws = content.split("// NODE LIST")
nodeListRaw = nodeListRaws[1]

cat      = ""
nodeData = {}
nodes    = {}

def extractNodeData(node):
    path = f"{scriptDir}\\{node}\\{node}.gml"
    with open(path, "r") as file:
        content = file.read()
    
    node = node.strip("_").lower()
    nodeName  = ""
    matchName = re.search(r"name\s*=\s*['\"](.*)['\"]", content)
    if matchName:
        nodeName = matchName.group(1)

    junctions = re.findall(r"nodeValue\((.*)\)", content)

    parent = "node"
    constructLine = re.search(r"function\s*" + node + r"(.*){", content, re.IGNORECASE)
    if constructLine and ":" in constructLine.group(1):
        parent = constructLine.group(1).split(":")[1].split("(")[0].strip()

    nodeData[node] = { "name": nodeName, "io": junctions, "parent": parent.lower() } 

for script in os.listdir(scriptDir):
    if script.strip("_").lower().startswith("node_"):
        extractNodeData(script)

def writeNodeFile(cat, node, line):
    if node.lower() not in nodeData:
        print(f"Node {node.lower()} not found in nodeData")
        return
    
    _data = nodeData[node.lower()]
    nodeName  = _data["name"]
    junctions = _data["io"]
    parent    = _data["parent"]
    
    basicData = '<tr><th class="head" colspan="2"><p>Node Data</p></th></tr>'

    basicData += f'<tr><th colspan="2" class="summary-topic"><p>Display name</p></th></tr>'
    basicData += f'<tr><th colspan="2" class="summary-content"><p>{nodeName}</p></th></tr>'
    
    basicData += f'<tr><th colspan="2" class="summary-topic"><p>Internal name</p></th></tr>'
    basicData += f'<tr><th colspan="2" class="summary-content"><p>{node}</p></th></tr>'

    p = parent
    parents = [ node.lower() ]

    while p in nodeData:
        _pdata = nodeData[p]
        junctions = _pdata["io"] + junctions
        parents.insert(0, p)
        
        p = nodeData[p]["parent"]
        if p == "node":
            break

    parents.insert(0, "node")
    
    basicData += '<tr height="8px"></tr>'
    basicData += '<tr><th class="head" colspan="2"><p>Inheritances</p></th></tr>'
    for p in parents:
        basicData += f'<tr><th colspan="2" class="inheritance-block"><p>{p}</p></th></tr>'

    className = node

    tooltip   = className
    createLine = line.split("(")[1].split(")")[0] # remove content inside [] to prevent comma miscount
    args = re.sub(r'\[.*?\]', '', createLine).split(",")
    if len(args) > 6:
        tooltip = args[6].strip().strip("\"")

    junctions = junc.IOTable(junctions)
    summary = basicData + '<tr height="8px"></tr>' + junctions

    txt = template.replace("{{nodeName}}", nodeName) \
                  .replace("{{tooltip}}", tooltip)   \
                  .replace("{{summary}}", summary)

    fileName = className.replace('Node_', '').lower()

    manFilePath = f"content/_nodes/{fileName}.html"
    if os.path.exists(manFilePath):
        with open(manFilePath, "r") as file:
            txt += file.read()
    else:
        with open(manFilePath, "w") as file:
            file.write("")

    filePath = f"content/{dirname}/{cat}/{fileName}.html"
    with open(filePath, "w") as file:
        file.write(txt)

for line in nodeListRaw.split("\n"):
    line = line.strip()

    if line.startswith("addNodeCatagory("):
        cat = line.split("\"")[1].lower()
        nodes[cat] = []
    elif line.startswith("addNodeObject("):
        args = line.split("(")[1].split(")")[0].split(",")

        nodeClass = args[3].strip().strip("\"")
        nodes[cat].append((nodeClass, line))

for cat in tqdm(nodes, leave = False):
    catPath = f"content/{dirname}/{cat}"
    if not os.path.exists(catPath):
        os.makedirs(catPath)

    txt = f"""<h1>{cat}</h1>"""
    filePath = f"content/{dirname}/{cat}/0_index.html"
    with open(filePath, "w") as file:
        file.write(txt)

    for node, line in nodes[cat]:
        writeNodeFile(cat, node, line)