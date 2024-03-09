import re

typeIndex = {
    "integer"      : 0,
	"float"        : 1,
	"boolean"      : 2,
	"color"        : 3,
	"surface"      : 4,
	
	"path"         : 5,
	"curve"        : 6,
	"text"         : 7,
	"object"       : 8,
	"node"         : 9,
	"d3object"     : 10,
	
	"any"          : 11,
	
	"pathnode"     : 12,
	"particle"     : 13,
	"rigid"        : 14,
	"sdomain"      : 15,
	"struct"       : 16,
	"strands"      : 17,
	"mesh"	       : 18,
	"trigger"      : 19,
	"atlas"	       : 20,
	
	"d3vertex"     : 21,
	"gradient"     : 22,
	"armature"     : 23,
	"buffer"       : 24,
	
	"pbBox"        : 25,
	
	"d3Mesh"       : 26,
	"d3Light"	   : 27,
	"d3Camera"     : 28,
	"d3Scene"	   : 29,
	"d3Material"   : 30,
	
	"dynaSurface"  : 31,
	"PCXnode"      : 32,
	
	"audioBit"     : 33,
	
	"fdomain"      : 34,
	
	"action"	   : 99,
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
]

def getColor(dataType):
    if dataType not in typeIndex:
        return "#8fde5d"

    ind = typeIndex[dataType]
    if ind >= len(typeColor) or ind < 0:
        return "#8fde5d"
    
    return typeColor[ind]

def IOTable(ioList):
    inputRows = ""
    outputRows = ""

    allio = {}
    
    for node, ios in ioList:
        _inputs  = []
        _inputDy = []
        _outputs = []

        inputPnt = _inputs

        for io in ios:
            if io == "[Dynamic]": 
                inputPnt = _inputDy
                continue
            
            io = io.strip()
            io = io.split(",")
            
            _name = io[0].strip()
            names = re.search(r'"(.*?)"', _name)
            if names:
                _name = names.group(1)

            _iotype = io[2].strip()
            _dataty = io[3].strip().replace("VALUE_TYPE.", "")

            if _iotype == "JUNCTION_CONNECT.input":
                inputPnt.append((_name, _dataty))
                
            elif _iotype == "JUNCTION_CONNECT.output":
                _outputs.append((_name, _dataty))

        for _name, _dataty in _inputs:
            allio[_name.lower()] = getColor(_dataty)
        for _name, _dataty in _inputDy:
            allio[_name.lower()] = getColor(_dataty)

        for _name, _dataty in _outputs:
            allio[_name.lower()] = getColor(_dataty)

        if _inputs:
            inputRows += f'<tr><th colspan="2" class="summary-topic"><p>{node}</p></th></tr>'

        inputRows += "".join([f"""<tr>
            <td class="summary-topic" style="width: 60px"><p style="color: {getColor(_dataty)}">{_dataty}</p></td>
            <td><p>{_name.title()}</p></td>
        </tr>""" for _name, _dataty in _inputs])

        if _inputDy:
            dynamicTable = f'''<table class="summary-table dynamic" style="margin-top: 8px;"><tr>
    <th colspan="2" class="summary-topic">
        <p style="margin: -0.85rem auto -4px auto;width: fit-content;padding: 0px 8px;">Dynamic Inputs</p>
    </th>
</tr>'''

            dynamicTable += "".join([f"""<tr>
                <td class="summary-topic" style="width: 60px"><p style="color: {getColor(_dataty)}" >{_dataty}</p></td>
                <td><p>{_name.title()}</p></td>
            </tr>""" for _name, _dataty in _inputDy])

            dynamicTable += "</table>"

            inputRows += f"""<tr><td colspan="2">{dynamicTable}</td></tr>"""

        if _outputs:
            outputRows += f'<tr><th colspan="2" class="summary-topic"><p>{node}</p></th></tr>'

        outputRows += "".join([f"""<tr>
            <td class="summary-topic" style="width: 60px"><p style="color: {getColor(_dataty)}">{_dataty}</p></td>
            <td><p>{_name.title()}</p></td>
        </tr>""" for _name, _dataty in _outputs])

    summaryTxt = f"""
<tr><th class="head" colspan="2"><p>Inputs</p></th></tr>
{inputRows}
<tr height="8px"></tr>
<tr><th class="head" colspan="2"><p>Outputs</p></th></tr>
{outputRows}
"""
    
    return (summaryTxt, allio)

def AttributeTable(attrList):
    rows = ""
    attributes = []

    for node, attrs in attrList:
        if attrs:
            rows += f'<tr><th colspan="2" class="summary-topic"><p>{node}</p></th></tr>'
            rows += "".join([f"""<tr><td colspan="2" class="summary-attribute"><p>{_attr}</p></td></tr>""" for _attr in attrs])

        attributes.append(attrs)
    
    if rows == "":
        return ("", attributes)
    
    summaryTxt = f"""
<tr><th class="head" colspan="2"><p>Attributes</p></th></tr>
{rows}
"""

    return (summaryTxt, attributes)