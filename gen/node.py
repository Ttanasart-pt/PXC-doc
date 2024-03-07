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
    
    matchNode = re.search(r"function\s(.*?)\(.*?\s:\s_*Node", content)
    node = "" if not matchNode else matchNode.group(1).lower()
    if not node.strip("_").startswith("node"):
        return
    if node in nodeData:
        return
    
    matchName = re.search(r"name\s*=\s*[\"](.*)[\"]", content)
    nodeName  = "" if not matchName else matchName.group(1)

    junctions  = re.findall(r"nodeValue\((.*)\)", content)

    parent = "node"
    constructLine = re.search(r"function\s*" + node + r"(.*){", content, re.IGNORECASE)
    if constructLine and ":" in constructLine.group(1):
        parent = constructLine.group(1).split(":")[1].split("(")[0].strip()

    attrs = re.findall(r'array_push\(attributeEditors, \["(.*?)"', content)
    attributes = []
    for a in attrs:
        attr = a.strip()
        if attr not in attributes:
            attributes.append(attr)

    nodeData[node] = { "name": nodeName, "io": junctions, "parent": parent.lower(), "attributes": attributes } 

for script in os.listdir(scriptDir):
    if script.strip("_").lower().startswith("node_"):
        extractNodeData(script)

def writeNodeFile(cat, node, line):
    if node.lower() not in nodeData:
        print(f"Node {node.lower()} not found in nodeData")
        return
    
    _data = nodeData[node.lower()]
    nodeName   = _data["name"]
    junctions  = [ ( node.lower(), _data["io"] ) ]
    parent     = _data["parent"]
    attributes = [ ( node.lower(), _data["attributes"] ) ]

    createLine = line.replace("\t", "").strip()
    createLine = createLine.split("(")[1].split(")")[0] # remove content inside [] to prevent comma miscount
    args = re.sub(r'\[.*?\]', '', createLine).split(",")

    spr = args[2].strip()
    _data["spr"] = spr
    
    basicData = '<tr><th class="head" colspan="2"><p>Node Data</p></th></tr>'
    basicData += f'<tr><th colspan="2"><img {spr}></th></tr>'

    basicData += f'<tr><th colspan="2" class="summary-topic"><p>Display name</p></th></tr>'
    basicData += f'<tr><th colspan="2" class="summary-content"><p>{nodeName}</p></th></tr>'
    
    basicData += f'<tr><th colspan="2" class="summary-topic"><p>Internal name</p></th></tr>'
    basicData += f'<tr><th colspan="2" class="summary-content"><p>{node}</p></th></tr>'

    p = parent
    parents = [ node.lower() ]

    while p in nodeData and p != "node":
        _pdata = nodeData[p]
        junctions.insert(0,  ( p, _pdata["io"] ))
        attributes.insert(0, ( p, _pdata["attributes"] ))
        parents.insert(0, p)
        
        p = nodeData[p]["parent"]

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
    tooltip   = "" if len(args) <= 6 else args[6].strip().strip("\"")
    summary   = basicData + '<tr height="8px"></tr>' + \
                    junc.IOTable(junctions) +          \
                    junc.AttributeTable(attributes)

    txt = template.replace("{{nodeName}}", nodeName) \
                  .replace("{{tooltip}}", tooltip)   \
                  .replace("{{summary}}", summary)

    fileName = className.replace('Node_', '').lower()
    
    manFilePath = f"content/__nodes/{fileName}.html"
    if os.path.exists(manFilePath):
        with open(manFilePath, "r") as file:
            content = file.read()
            nodeTags = re.findall(r'<node\s(.*?)>', content)
            for tag in nodeTags:
                name = tag
                if "node_" + tag in nodeData:
                    name = nodeData["node_" + tag]["name"]

                content = content.replace(f'<node {tag}>', f'<a href="../_index/{tag}.html">{name}</a>')
            txt += content
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
        
    return { "spr": spr }

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

def generateNodeCatagory(cat):
    txt = f"""<h1>{cat.title()}</h1>
<br><br>
<img node_cat_{cat}>
<br>
<div class=node-group>"""
    
    nodeNames = [ node for node, _ in nodes[cat] ]
    nodeNames.sort()

    for node in nodeNames:
        _data = nodeData[node.lower()]
        spr   = _data["spr"]
        name  = _data["name"]

        txt += f'''<div>
<a href="./{node.lower().replace("node_", "")}.html"><img {spr}>{name}</a>
</div>\n'''

    txt += "</div>"
    
    filePath = f"content/{dirname}/{cat}/0_index.html"
    with open(filePath, "w") as file:
        file.write(txt)

for cat in nodes:
    catPath = f"content/{dirname}/{cat}"
    if not os.path.exists(catPath):
        os.makedirs(catPath)

    for node, line in nodes[cat]:
        writeNodeFile(cat, node, line)

    generateNodeCatagory(cat)