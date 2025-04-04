# %%
import os
import shutil
import re
from enum import Enum

import fileUtil

class FileType(Enum):
    FILE  = 0
    DIR   = 1
    BACK  = 2

def title(s): # Replace _ with space and capitalize the first letter in each word
    return s.replace('_', ' ').title()

def pathStrip(path): # Strip out the custom ordering n_ at the start of the file
    name = os.path.basename(path)
    if name.split("_")[0].isdigit():
        name = name[name.find('_') + 1:]
    return os.path.join(os.path.dirname(path), name)
    
# %% Copy image files
nodeIconDir = "D:/Project/MakhamDev/LTS-PixelComposer/RESOURCE/nodeIcons"
shutil.copytree(nodeIconDir, "../src/nodeIcons", dirs_exist_ok = True)
shutil.copytree("../src", "../docs/src", dirs_exist_ok = True)

images = {}
for root, dirs, files in os.walk("../src"):
    for file in files:
        if not file.endswith(".png"):
            continue

        key = file[:-4].lower()
        images[key] = os.path.join(root, file).replace("\\", "/")

template = fileUtil.readFile("../templates/page.html")

# %%
svg_home = fileUtil.readFile("../src/svg/home.svg")
svg_dir  = fileUtil.readFile("../src/svg/dir.svg")
pages    = []

def generateFile(dirOut, pathIn, sidebar):
    with open(pathIn, "r") as f:
        content = f.read()

    pathIn    = pathStrip(pathIn)
    fileName  = os.path.basename(pathIn)
    pathOut   = f"{dirOut}\\{fileName}"
    headers   = []
    badges    = ""

    version = re.findall(r"<v (.*?)>", content)
    if len(version) > 0:
        version = version[0]
        content = content.replace(f"<v {version}>", "")

        version = version.strip("/").strip()
        badges += f'<p class="version-banner" title="Updated for version {version}">{version}</p>'
    else:
        badges += f'<p class="version-banner" title="Writen before 1.18, some information might be outdated">pre 1.18</p>'

    h1s = re.findall(r"<h1>(.*?)</h1>", content)
    if len(h1s) > 0:
        h1 = h1s[0]
        content = content.replace(f"<h1>{h1}</h1>", f'''<div class="title">
                                                            <h1>{h1}</h1>
                                                            <div class="badges">{badges}</div>
                                                        </div>''')
        

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

        if imgraw.lower() in images:
            content = content.replace(f"<img {img}>", f'<img class="node-content" src="/{images[imgraw.lower()]}">')
        elif "=" not in imgraw: 
            print(f"{pathOut} : Image {imgraw} not found")

    imgs = re.findall(r"<img-deco (.*?)>", content)
    for img in imgs:
        imgraw = img.strip("/")

        if imgraw.lower() in images:
            content = content.replace(f"<img-deco {img}>", f'<img class="node-content deco" src="/{images[imgraw.lower()]}">')
        elif "=" not in imgraw: 
            print(f"{pathOut} : Image {imgraw} not found")

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

    with open(pathOut, "w") as f:
        f.write(data)

    title = fileName.replace('.html', '').replace('_', ' ').title()
    pages.append((title, pathOut))

def generateFolder(dirIn, dirOut):
    files   = sorted(os.listdir(dirIn))
    sidebar = []

    if dirIn == "../pregen":
        groupTitle = "Home"
        sidebar.append((FileType.BACK, "", "", ""))
    else:
        groupTitle = os.path.basename(dirIn)
        groupTitle = title(pathStrip(groupTitle))
        sidebar.append((FileType.BACK, "../", "../", "Back"))
    
    if not os.path.exists(dirOut):
        os.mkdir(dirOut)

    for fName in files:
        if fName.startswith("_"):
            continue
        
        fullPath = os.path.join(dirIn, fName)
        fNameS   = pathStrip(fName)
        pTitle   = title(fNameS)
        
        if os.path.isdir(fullPath):
            sidebar.append((FileType.DIR, fName, fNameS, pTitle))

        elif fullPath.endswith(".html"):
            pTitle = pTitle.replace('.Html', '')
            if pTitle == "Index":
                pTitle = groupTitle
                sidebar.insert(0, (FileType.FILE, fName, fNameS, pTitle))
            else:
                sidebar.append((FileType.FILE, fName, fNameS, pTitle))

        elif fullPath.endswith(".md"):
            continue   
        
        else :
            shutil.copy(fullPath, os.path.join(dirOut, fName))

    for fType, fName, fNameS, _ in sidebar[1:]:
        fDirIn  = os.path.join(dirIn,  fName)
        fDirOut = os.path.join(dirOut, fNameS)

        if fType == FileType.DIR:
            generateFolder(fDirIn, fDirOut)
        elif fType == FileType.FILE:
            generateFile(dirOut, fDirIn, sidebar)

generateFolder("../pregen", "../docs")
shutil.copy("../styles.css", "../docs/styles.css")

# %% generate static search
search_list_str = ""
for title, path in pages:
    if title == "Index":
        continue

    real_path = path.replace("../docs\\", "\\")
    search_list_str += f'<li class="search-result" style="display: none;"><a href="{real_path}">{title}</a></li>\n'

for _, path in pages:
    with open(path, "r") as f:
        content = f.read()
    content  = content.replace("{{search_results}}", search_list_str)
    with open(path, "w") as f:
        f.write(content)