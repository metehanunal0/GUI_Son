import os

direc = "./"
files = os.listdir(direc)
filelist = list()

for i in files:
    if i[-3:] == ".ui":
        filelist.append(i)

for i in filelist:
    os.system(f"cd {direc} & pyuic5 {i} -o {i[:-3]}.py")
    print(f"Converted {i} to {i[:-3]}.py")