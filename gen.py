import os
import shutil
from re import sub

root = "content"
templatePath = "template.html"

with open(templatePath, "r") as f:
    template = f.read()

def camel(s):
    return sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', s)

def pathStrip(path):
    name = os.path.basename(path)
    if name[0].isdigit():
        name = name[name.find('_') + 1:]
    return os.path.join(os.path.dirname(path), name)

def generateFile(path, sidebar):
    with open(path, "r") as f:
        content = f.read()

    path      = pathStrip(path)
    outPath   = f"docs/{path.replace(root, '').lower()}"
    fileName  = os.path.basename(path)

    sideContent = ""
    for s in sidebar:
        if s[0] == fileName :
            sideContent += f'<li><a class="active" href="{s[0].lower()}">{s[1]}</a></li>\n'
        else :
            sideContent += f'<li><a href="{s[0].lower()}">{s[1]}</a></li>\n'

    data = template.replace("{{content}}", content)
    data = data.replace("{{sidebar}}", sideContent)

    with open(outPath, "w") as f:
        f.write(data)

def generateFolder(path):
    files = os.listdir(path)
    
    dirPath = f"docs/{path.replace(root, '')}"
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)

    sidebar = []
    for f in files:
        if f.endswith(".html"):
            f = pathStrip(f)

            title = f.replace('.html', '')
            title = camel(title)
            if title == "Index":
                title = "Home"

            sidebar.append((f, title))

    for f in files:
        fullPath = os.path.join(path, f)

        if os.path.isdir(fullPath):
            generateFolder(fullPath)
        elif fullPath.endswith(".html"):
            generateFile(fullPath, sidebar)

generateFolder(root)

shutil.copy("styles.css", "docs/styles.css")