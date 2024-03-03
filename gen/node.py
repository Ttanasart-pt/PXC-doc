import os
import re

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

if not os.path.exists("docs/nodes"):
    os.makedirs("docs/nodes")
if not os.path.exists("docs/nodes/_index"):
    os.makedirs("docs/nodes/_index")
if not os.path.exists("docs/nodes/_index/index.html"):
    with open("docs/nodes/_index/index.html", "w") as file:
        file.write(f'''<!DOCTYPE html><html></html>''')

nodeListRaws = content.split("// NODE LIST")
nodeListRaw = nodeListRaws[1]

cat       = ""
nodeData  = {}
nodePages = {}
nodes     = {}

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
    junctions = [ ( node.lower(), _data["io"] ) ]
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
        junctions.insert(0, ( p, _pdata["io"] ))
        parents.insert(0, p)
        
        p = nodeData[p]["parent"]
        if p == "node":
            break

    parents.insert(0, "node")
    
    basicData += '<tr height="8px"></tr>'
    basicData += '<tr><th class="head" colspan="2"><p>Inheritances</p></th></tr>'
    for i, p in enumerate(parents):
        link = ""
        if p == "node":
            link = "../index.html"
        elif p == "node_processor":
            link = "../array_processor.html"
        elif p in nodePages:
            link = f"../_index/{p[5:]}.html"
        
        _class = "inheritance-block current" if i == len(parents) - 1 else "inheritance-block"

        if link == "":
            basicData += f'<tr><th colspan="2" class="{_class}"><p>{p}</p></th></tr>'
        else:
            basicData += f'<tr><th colspan="2" class="{_class}"><a href="{link}">{p}</a></th></tr>'

    className = node

    tooltip   = ""
    createLine = line.split("(")[1].split(")")[0] # remove content inside [] to prevent comma miscount
    args = re.sub(r'\[.*?\]', '', createLine).split(",")
    if len(args) > 6:
        tooltip = args[6].strip().strip("\"")

    junctionList = junc.IOTable(junctions)
    summary = basicData + '<tr height="8px"></tr>' + junctionList

    txt = template.replace("{{nodeName}}", nodeName) \
                  .replace("{{tooltip}}", tooltip)   \
                  .replace("{{summary}}", summary)

    fileName = className.replace('Node_', '').lower()

    manFilePath = f"content/__nodes/{fileName}.html"
    if os.path.exists(manFilePath):
        with open(manFilePath, "r") as file:
            txt += file.read()
    else:
        with open(manFilePath, "w") as file:
            file.write("")

    filePath = f"content/{dirname}/{cat}/{fileName}.html"
    with open(filePath, "w") as file:
        file.write(txt)

    redirectPath = f"docs/nodes/_index/{fileName}.html"
    with open(redirectPath, "w") as file:
        file.write(f'''<!DOCTYPE html>
<html>
    <meta http-equiv="refresh" content="0; url=/nodes/{cat}/{fileName}.html"/>
</html>''')

for line in nodeListRaw.split("\n"):
    line = line.strip()

    if line.startswith("addNodeCatagory("):
        cat = line.split("\"")[1].lower()
        nodes[cat] = []
    elif line.startswith("addNodeObject("):
        args = line.split("(")[1].split(")")[0].split(",")

        nodeClass = args[3].strip().strip("\"")
        nodes[cat].append((nodeClass, line))

        nodePages[nodeClass.lower()] = 1

for cat in nodes:
    catPath = f"content/{dirname}/{cat}"
    if not os.path.exists(catPath):
        os.makedirs(catPath)

    txt = f"""<h1>{cat.title()}</h1>"""
    filePath = f"content/{dirname}/{cat}/0_index.html"
    with open(filePath, "w") as file:
        file.write(txt)

    for node, line in nodes[cat]:
        writeNodeFile(cat, node, line)