import os
import shutil
from re import sub
from enum import Enum
from tqdm import tqdm

class FileType(Enum):
    FILE = 0
    DIR  = 1
    BACK = 2

templatePath = "templates/page.html"
with open(templatePath, "r") as f:
    template = f.read()

def space(s): # Replace _ with space and capitalize the first letter in each word
    s = s.replace('_', ' ')
    return s.title()

def pathStrip(path): # Strip out the custom ordering n_ at the start of the file
    name = os.path.basename(path)
    if name.split("_")[0].isdigit():
        name = name[name.find('_') + 1:]
    return os.path.join(os.path.dirname(path), name)

def loadFile(path):
    with open(path, "r") as f:
        return f.read()
    
svg_home = loadFile("src/svg/home.svg")
svg_dir = loadFile("src/svg/dir.svg")

def generateFile(dirOut, pathIn, sidebar):
    with open(pathIn, "r") as f:
        content = f.read()

    pathIn    = pathStrip(pathIn)
    fileName  = os.path.basename(pathIn)
    outPath   = f"{dirOut}\\{fileName}"

    sideContent = ""
    for fType, _, fName, title in sidebar:
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

def generateFolder(dirIn, dirOut):
    files = os.listdir(dirIn)
    sidebar = []

    if dirIn == "content":
        groupTitle = "Home"
        sidebar.append((FileType.BACK, "", "", ""))
    else:
        groupTitle = os.path.basename(dirIn)
        groupTitle = space(pathStrip(groupTitle))
        sidebar.append((FileType.BACK, "../", "../", "Back"))
    
    if not os.path.exists(dirOut):
        os.mkdir(dirOut)

    for f in files:
        if f.startswith("_"):
            continue
        
        fullPath = os.path.join(dirIn, f)
        fs = pathStrip(f)
        title = space(fs)
        
        if os.path.isdir(fullPath):
            sidebar.append((FileType.DIR, f, fs, title))

        elif fullPath.endswith(".html"):
            title = title.replace('.Html', '')
            if title == "Index":
                title = groupTitle

            sidebar.append((FileType.FILE, f, fs, title))

    for t, f, fs, _ in sidebar[1:]:
        fDirIn = os.path.join(dirIn, f)
        fDirOut = os.path.join(dirOut, fs)

        if t == FileType.DIR:
            generateFolder(fDirIn, fDirOut)
        elif t == FileType.FILE:
            generateFile(dirOut, fDirIn, sidebar)

generateFolder("content", "docs")

shutil.copy("styles.css", "docs/styles.css")