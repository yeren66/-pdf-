import os
path = "D:\\phthon专用\\20210901\\PDF\\"
name = os.listdir(path)
for i in range(len(name)):
    os.rename(path + name[i], path + str(i) + " " + name[i])