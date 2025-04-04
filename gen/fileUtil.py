import os

def pathStrip(path): # Strip out the custom ordering n_ at the start of the file
    if path.split("_")[0].isdigit():
        path = path[path.find('_') + 1:]
    return path.title()

def pathSanitize(path):
    path = path.replace(" ", "_") \
               .replace("(", "_") \
               .replace(")", "_") \
               .replace("-", "_") \
               .replace("/", "")  \
               .lower()
    return path

# %%

def verifyFolder(path):
    path = os.path.abspath(path)
    p = path
    f = []

    while not os.path.exists(p):
        f.append(p)
        p = os.path.dirname(p)
        if p == "":
            break

    for folder in f[::-1]:
        os.mkdir(folder)

def verifyFile(path, content = ""):
    verifyFolder(os.path.dirname(path))

    if not os.path.exists(path):
        with open(path, "w") as file:
            file.write(content)

def writeFile(path, content):
    with open(path, "w") as file:
        file.write(content)