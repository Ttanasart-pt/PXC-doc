import os
import shutil

shutil.copytree("content", "pregen")

print("Runing md.py...")
os.system("python gen/md.py")

print("Runing nodes.py...")
os.system("python gen/node.py")

print("Runing gen.py...")
os.system("python gen/gen.py")

shutil.rmtree("pregen")