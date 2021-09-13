import re
from skimage import io
from PIL import Image
import ast
import numpy as np


office_path = "picture.txt"
path = "D:\\phthon专用\\20210901\\picture\\"
new_path = "D:\\phthon专用\\20210901\\PDF\\"


q = 0
with open(office_path, 'r', encoding='utf8') as file:
    while True:
        q += 1
        lines = file.readline()
        if not lines:
            break
        name = re.search('(.*?).jpg', lines)  # use name.group() to get address of file
        infor = re.search('{(.*)}', lines)
        infor_dict = ast.literal_eval(infor.group())  # infor_dict contains the information of pdf

        img = io.imread(path + name.group())
        t = np.mean(img)
        img = Image.open(path + name.group())
        img = img.point(lambda x: 0 if x > t else 255)  # 0 代表黑， 255代表白
        img = img.convert('1')
        img.save(new_path + name.group())
        print(q)