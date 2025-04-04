# %%
import os
import fileUtil

import nodeParser
import juncWriter

with open("../templates/node.html", "r") as f:
    template = f.read()

def generateBadge(title, tooltip, color, page = ""):
    style = f"color: #{color}; background-color: #{color}16; border-color: #{color}60;"
    return f'<a href="{page}" class="badge" style="{style}" title="{tooltip}">{title}</a>'

def generateBasicData(nodeData, metadata):  
    nodeName   = metadata["name"]
    node       = metadata["baseNode"]
    spr        = metadata["spr"]     if "spr" in metadata else f"s_{node.lower()}"

    categories = nodeData["categories"]
    parents    = nodeData["inheritances"]

    basicData = '<tr><th class="head" colspan="2"><p>Node Data</p></th></tr>'
    basicData += f'<tr><th colspan="2"><img {spr}></th></tr>'

    badges = ""
    for btitle, bdesp, bcolor, bpage in categories:
        badges += generateBadge(btitle, bdesp, bcolor, bpage)

    if badges != "":
        basicData += '<tr style="height: 4px;"></tr>'
        basicData += f'<tr><th colspan="2">{badges}</th></tr>'
        basicData += '<tr style="height: 8px;"></tr>'

    basicData += f'<tr><th colspan="2" class="summary-topic"><p>Display name</p></th></tr>'
    basicData += f'<tr><th colspan="2" class="summary-content"><p>{nodeName}</p></th></tr>'
    
    basicData += f'<tr><th colspan="2" class="summary-topic"><p>Internal name</p></th></tr>'
    basicData += f'<tr><th colspan="2" class="summary-content"><p>{node}</p></th></tr>'
    
    basicData += '<tr height="8px"></tr>'
    basicData += '<tr><th class="head" colspan="2"><p>Inheritances</p></th></tr>'

    for i, p in enumerate(parents):
        pName = p["name"]
        link  = ""

        if pName == "Node":
            link = "../index.html"
        elif pName == "Node_Processor":
            link = "../array_processor.html"
        else:
            link = f"../_index/{pName}.html"
        
        _class = "inheritance-block current" if i == len(parents) - 1 else "inheritance-block"

        basicData += f'<tr><th colspan="2" class="{_class}"><a href="{link}">{pName}</a></th></tr>'
    return basicData

def applySummaryTable(basicData, junctionText, attributeText):
    return basicData + '<tr height="8px"></tr>' + \
           junctionText +                         \
           attributeText

def applyTemplate(template, nodeName, tooltip, summary):
    return template.replace("{{nodeName}}", nodeName) \
                   .replace("{{tooltip}}",  tooltip)  \
                   .replace("{{summary}}",  summary)

def writeNode(metadata, contentPath):
    with open(contentPath, "r") as f:
        rawContent = f.read()

    nodeName = metadata["name"]
    nodeBase = metadata["baseNode"]
    tooltip  = metadata["tooltip"] if "tooltip" in metadata else ""
    nodeData = nodeParser.getNodeData(nodeBase)

    if not nodeData:
        print(f"Node data for {nodeBase} not found.")
        return None
    
    print(f"Generating node file for {nodeName}")

    basicData     = generateBasicData(nodeData, metadata)
    junctionText  = juncWriter.IOTable(nodeData)
    attributeText = juncWriter.AttributeTable(nodeData)

    summary  = applySummaryTable(basicData, junctionText, attributeText)
    content  = applyTemplate(template, nodeName, tooltip, summary)

    content += rawContent
    return content

# %%
group_start = '''<div class="node-group">'''
group_end   = '''</div>'''

def writeCategory(category, nodeMetadata):
    name  = category["name"]
    nodes = category["nodes"]

    title   = name
    content = f"""<h1>{title}</h1><br><br>"""
    nl = True
    
    for node in nodes:
        if not isinstance(node, str):
            subGroup = node["label"]
            sgName   = subGroup.strip("/")
            sgLevel  = "h4" if subGroup.startswith("/") else "h3"

            if not nl:
                content += group_end
            content += f'<{sgLevel}>{sgName}</{sgLevel}>'
            nl = True
            continue

        if node not in nodeMetadata:
            print(f"Node content for {node} not found.")
            continue
        
        if nl:
            content += group_start
            nl = False

        metadata = nodeMetadata[node]
        name     = metadata["name"]
        spr      = metadata["spr"]  if "spr" in metadata else f"s_{node.lower()}"

        content += f'''<div><a href="./{node.lower().replace("node_", "")}.html"><img {spr}>{name}</a></div>\n'''

    if not nl:
        content += group_end
    return content