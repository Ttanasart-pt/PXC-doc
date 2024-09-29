import os
import shutil

print("Runing nodes.py...")
os.system("python gen/node.py")

print("Runing gen.py...")
os.system("python gen/gen.py")