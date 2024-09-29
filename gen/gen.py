import os
import shutil
import re
from enum import Enum

class FileType(Enum):
    FILE  = 0
    DIR   = 1
    BACK  = 2

shutil.copytree("src", "docs/src", dirs_exist_ok = True)

images = {}
for root, dirs, files in os.walk("src"):
    for file in files:
        if file.endswith(".png"):
            images[file[:-4]] = os.path.join(root, file).replace("\\", "/")

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
pages = []

def generateFile(dirOut, pathIn, sidebar):
    with open(pathIn, "r") as f:
        content = f.read()

    pathIn    = pathStrip(pathIn)
    fileName  = os.path.basename(pathIn)
    outPath   = f"{dirOut}\\{fileName}"
    headers   = []

    for h2s in content.split("<h2>")[1:]:
        h2  = h2s.split("</h2>")[0]
        h3s = re.findall(r"<h3>(.*?)</h3>", h2s)
        
        content = content.replace(f"<h2>{h2}</h2>", f'<h2><a id="{h2}" class="anchor"></a>{h2}</h2>')
        for i, _h3 in enumerate(h3s):
            h3 = re.sub(r'<(.*?)\/.*?>', '', _h3)
            if h3 == "":
                h3 = re.sub(r'<.*?>', '', _h3)
            h3s[i] = h3
            content = content.replace(f"<h3>{_h3}</h3>", f'<h3><a id="{h3}" class="anchor"></a>{_h3}</h3>')

        headers.append({"h2": h2, "h3s": h3s})

    imgs = re.findall(r"<img (.*?)>", content)
    for img in imgs:
        imgraw = img.strip("/")

        if imgraw in images:
            content = content.replace(f"<img {img}>", f'<img class="node-content" src="/{images[imgraw]}">')
        elif '"' not in img: 
            print(f"{pathIn} : Image {imgraw} not found")

    imgs = re.findall(r"<img-deco (.*?)>", content)
    for img in imgs:
        imgraw = img.strip("/")

        if imgraw in images:
            content = content.replace(f"<img-deco {img}>", f'<img class="node-content deco" src="/{images[imgraw]}">')
        elif '"' not in img: 
            print(f"{pathIn} : Image {imgraw} not found")

    nodeTags = re.findall(r'<node\s(.*?)>', content)
    for tag in nodeTags:
        name = tag.strip("/")
        content = content.replace(f'<node {tag}>', f'<a class="node" href="/nodes/_index/{name}.html">{name.title()}</a>')

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

        sideContent += f'<li class="sidebar-nav {liClass}">{icon}<a class="{aClass}" href="{fName}">{title}</a></li>\n'

        if fName == fileName :
            sideContent += '<ul class="submenu">\n'
            for h2 in headers:
                title = h2["h2"]
                sideContent += f'<li class="sidebar-nav"><a href="#{title}">{title}</a></li>\n'

                sideContent += '<ul class="submenu h3">\n'
                for h3 in h2["h3s"]:
                    sideContent += f'<li class="sidebar-nav"><a href="#{h3}">{h3}</a></li>\n'
                sideContent += "</ul>\n"

            sideContent += "</ul>\n"

    data = template.replace("{{content}}", content)
    data = data.replace("{{sidebar}}", sideContent)

    with open(outPath, "w") as f:
        f.write(data)

    title = fileName.replace('.html', '').replace('_', ' ').title()
    pages.append((title, outPath))

def generateFolder(dirIn, dirOut):
    files = sorted(os.listdir(dirIn))
    sidebar = []

    if dirIn == "pregen":
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

        else :
            shutil.copy(fullPath, os.path.join(dirOut, f))

    for t, f, fs, _ in sidebar[1:]:
        fDirIn = os.path.join(dirIn, f)
        fDirOut = os.path.join(dirOut, fs)

        if t == FileType.DIR:
            generateFolder(fDirIn, fDirOut)
        elif t == FileType.FILE:
            generateFile(dirOut, fDirIn, sidebar)

generateFolder("pregen", "docs")

# search
search_list_str = ""
for title, path in pages:
    if title == "Index":
        continue

    real_path = path.replace("docs\\", "\\")
    search_list_str += f'<li class="search-result" style="display: none;"><a href="{real_path}">{title}</a></li>\n'

for _, path in pages:
    with open(path, "r") as f:
        content = f.read()
    content  = content.replace("{{search_results}}", search_list_str)
    with open(path, "w") as f:
        f.write(content)