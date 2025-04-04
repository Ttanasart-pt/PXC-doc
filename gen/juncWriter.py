import re

dispIndex = {
    "dimension"       : "integer",
    "enum_button"     : "integer",
    "enum_scroll"     : "integer",
    "int"             : "integer",
    "toggle"          : "integer",
    "area"            : "float",
    "corner"          : "float",
    "padding"         : "float",
    "palette"         : "color",
    "path_anchor"     : "float",
    "path_anchor_3d"  : "float",
    "quaternion"      : "float",
    "range"           : "float",
    "rotation"        : "float",
    "rotation_random" : "float",
    "rotation_range"  : "float",
    "slider_range"    : "float",
    "vec2"            : "float",
    "vec2_range"      : "float",
    "vec3"            : "float",
    "vec3_range"      : "float",
    "vec4"            : "float",
    "vector"          : "float",
    "bool"            : "boolean",
}

typeIndex = {
	"integer"     :  0,
	"float"       :  1,
	"boolean"     :  2,
	"color"       :  3,
	"surface"     :  4,
	
	"path"        :  5,
	"curve"       :  6,
	"text"        :  7,
	"object"      :  8,
	"node"        :  9,
	"d3object"    : 10,
	
	"any"         : 11,
	
	"pathnode"    : 12,
	"particle"    : 13,
	"rigid"       : 14,
	
	"sdomain"     : 15,
	"struct"      : 16,
	"strands"     : 17,
	"mesh"        : 18,
	"trigger"     : 19,
	"atlas"       : 20,
	
	"d3vertex"    : 21,
	"gradient"    : 22,
	"armature"    : 23,
	"buffer"      : 24,
	
	"pbbox"       : 25,
	
	"d3mesh"      : 26,
	"d3light"     : 27,
	"d3camera"    : 28,
	"d3scene"     : 29,
	"d3material"  : 30,
	
	"dynasurface" : 31,
	"pcxnode"     : 32,
	"audiobit"    : 33,
	"fdomain"     : 34,
	"sdf"         : 35,
	
	"action"      : 99,
}

typeColor = [
    "#ff9166",
    "#ffe478",
    "#8c3f5d",
    "#8fde5d",
    "#ff6b97",
    "#eb004b",
    "#c2c2d1",
    "#66ffe3",
    "#ffb5b5",
    "#4da6ff",
    "#c1007c",
    "#808080",
    "#ffb5b5",
    "#8fde5d",
    "#88ffe9",
    "#6d6e71",
    "#8c3f5d",
    "#ff9166",
    "#c2c2d1",
    "#8fde5d",
    "#ff6b97",
    "#c1007c",
    "#8fde5d",
    "#ff9166",
    "#808080",
    "#ff6b97",
    "#4da6ff",
    "#4da6ff",
    "#4da6ff",
    "#4da6ff",
    "#ff6b97",
    "#ff6b97",
    "#c2c2d1",
    "#8fde5d",
    "#4da6ff",
    "#c1007c",
]

def getColor(dataType):
    dtype = dataType
    if dtype in dispIndex:
        dtype = dispIndex[dtype]

    if dtype not in typeIndex:
        return "#8fde5d"

    ind = typeIndex[dtype]
    if ind >= len(typeColor) or ind < 0:
        return "#8fde5d"
    
    return typeColor[ind]

def IOTable(nodeData):
    parents    = nodeData["parents"]
    inputRows  = ""
    outputRows = ""
    allio      = {}
    
    for node in parents:
        _name    = node["name"]
        _inputs  = node["inputs"]
        _outputs = node["outputs"]
        
        for _junc in _inputs:
            allio[_junc["name"]] = getColor(_junc["type"])
        
        for _junc in _outputs:
            allio[_junc["name"]] = getColor(_junc["type"])

        if _inputs:
            inputRows += f'<tr><th colspan="2" class="summary-topic"><p>{_name}</p></th></tr>'

        for _junc in _inputs:
            # mapStr = "" if not _mappable else '<a href="/nodes/junctions/mappable.html" style="line-height: 1;"><img mappable></a>'
            mapStr = ""
            jName  = _junc["name"]
            jType  = _junc["type"]

            inputRows += f"""<tr>
                <td class="summary-topic" style="width: 60px"><p style="color: {getColor(jType)}">{jType}</p></td>
                <td><p>{jName.title()}{mapStr}</p></td>
            </tr>"""

        # if _inputDy:
        #     dynamicTable = f'''<table class="summary-table dynamic" style="margin-top: 8px;"><tr>
        #         <th colspan="2" class="summary-topic">
        #             <p style="margin: -0.85rem auto -4px auto;width: fit-content;padding: 0px 8px;">Dynamic Inputs</p>
        #         </th>
        #     </tr>'''

        #     for _name, _dataty, _mappable in _inputDy:
        #         dynamicTable += f"""<tr>
        #             <td class="summary-topic" style="width: 60px"><p style="color: {getColor(_dataty)}" >{_dataty}</p></td>
        #             <td><p>{_name.title()}</p></td>
        #         </tr>"""

        #     dynamicTable += "</table>"

        #     inputRows += f"""<tr><td colspan="2">{dynamicTable}</td></tr>"""

        if _outputs:
            outputRows += f'<tr><th colspan="2" class="summary-topic"><p>{node}</p></th></tr>'

        for _junc in _outputs:
            jName  = _junc["name"]
            jType  = _junc["type"]

            outputRows += f"""<tr>
                <td class="summary-topic" style="width: 60px"><p style="color: {getColor(jType)}">{jType}</p></td>
                <td><p>{jName.title()}</p></td>
            </tr>"""

    summaryTxt = f"""
<tr><th class="head" colspan="2"><p>Inputs</p></th></tr>
{inputRows}
<tr height="8px"></tr>
<tr><th class="head" colspan="2"><p>Outputs</p></th></tr>
{outputRows}
"""
    
    return summaryTxt

def AttributeTable(nodeData):
    attributes = []
    attrList   = nodeData["attributes"]
    rows       = ""

    for node, attrs in attrList:
        if attrs:
            rows += f'<tr><th colspan="2" class="summary-topic"><p>{node}</p></th></tr>'
            rows += "".join([f"""<tr><td colspan="2" class="summary-attribute"><p>{_attr}</p></td></tr>""" for _attr in attrs])

        attributes.append(attrs)
    
    if rows == "":
        return ""
    
    summaryTxt = f"""
<tr><th class="head" colspan="2"><p>Attributes</p></th></tr>
{rows}
"""

    return summaryTxt