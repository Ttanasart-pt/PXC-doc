import os
import shutil
from re import sub
from enum import Enum

class FileType(Enum):
    FILE = 0
    DIR  = 1
    BACK = 2

root = "content"
templatePath = "template.html"

with open(templatePath, "r") as f:
    template = f.read()

def space(s): # Replace _ with space and capitalize the first letter in each word
    s = s.replace('_', ' ')
    return s.title()

def pathStrip(path):
    name = os.path.basename(path)
    if name[0].isdigit():
        name = name[name.find('_') + 1:]
    return os.path.join(os.path.dirname(path), name)

def loadFile(path):
    with open(path, "r") as f:
        return f.read()
    
svg_home = loadFile("src/svg/home.svg")
svg_dir = loadFile("src/svg/dir.svg")

def generateFile(path, sidebar):
    with open(path, "r") as f:
        content = f.read()

    path      = pathStrip(path)
    outPath   = f"docs/{path.replace(root, '').lower()}"
    fileName  = os.path.basename(path).lower()

    sideContent = ""
    for s in sidebar:
        fType = s[0]
        fName = s[1]
        title = s[2]

        aClass  = ""
        liClass = ""
        icon    = ""

        if fType == FileType.DIR:
            icon = svg_dir

        elif fType == FileType.FILE:
            if fName == fileName :
                liClass += "active "
            if fName == "index.html":
                icon = svg_home

        elif fType == FileType.BACK:
            liClass += "back "
        
        if icon != "":
            liClass += "icon "

        sideContent += f'<li class="{liClass}">{icon}<a class="{aClass}" href="{fName}">{title}</a></li>\n'

    data = template.replace("{{content}}", content)
    data = data.replace("{{sidebar}}", sideContent)

    with open(outPath, "w") as f:
        f.write(data)

def generateFolder(path, parent = ""):
    files = os.listdir(path)
    sidebar = []

    if parent == "":
        groupTitle = "Home"
        sidebar.append((FileType.BACK, "", ""))
    else:
        groupTitle = os.path.basename(path)
        groupTitle = pathStrip(space(groupTitle))
        sidebar.append((FileType.BACK, "../", "Back"))
    
    dirPath = f"docs/{path.replace(root, '')}"
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)

    for f in files:
        fullPath = os.path.join(path, f)
        f = pathStrip(f)

        if os.path.isdir(fullPath):
            title = space(f)
            sidebar.append((FileType.DIR, f.lower(), title))

        elif fullPath.endswith(".html"):
            title = f.replace('.html', '')
            title = space(title)
            if title == "Index":
                title = groupTitle

            sidebar.append((FileType.FILE, f.lower(), title))

    for f in files:
        fullPath = os.path.join(path, f)
        if f.startswith("_"):
            continue

        if os.path.isdir(fullPath):
            generateFolder(fullPath, path)
        elif fullPath.endswith(".html"):
            generateFile(fullPath, sidebar)

generateFolder(root)

shutil.copy("styles.css", "docs/styles.css")