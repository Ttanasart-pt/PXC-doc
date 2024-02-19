import os
import shutil
from re import sub

root = "content"
templatePath = "template.html"

with open(templatePath, "r") as f:
    template = f.read()

def camel(s):
    return sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', s)

def generateFile(path, sidebar):
    outPath   = f"doc/{path.replace(root, '')}"

    with open(path, "r") as f:
        content = f.read()

    data = template.replace("{{content}}", content)
    data = data.replace("{{sidebar}}", sidebar)

    with open(outPath, "w") as f:
        f.write(data)

def generateFolder(path):
    files = os.listdir(path)
    sidebar = ""

    os.mkdir(f"doc/{path.replace(root, '')}")

    for f in files:
        if f.endswith(".html"):
            title = f.replace('.html', '')
            title = camel(title)

            sidebar += f"<a href='{f}'>{title}</a>"

    for f in files:
        fullPath = os.path.join(path, f)

        if os.path.isdir(fullPath):
            generateFolder(fullPath)
        elif fullPath.endswith(".html"):
            generateFile(fullPath, sidebar)

if os.path.exists("doc"):
    shutil.rmtree("doc")

generateFolder(root)