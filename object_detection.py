# coding: utf-8

from PIL import ImageDraw
from PIL import Image
import os
import re
import ast

office_path = "picture.txt"
path = "D:\\phthon专用\\20210901\\pdf_new\\"
path_1 = "D:\\phthon专用\\20210901\\pdf_new\\99 南京大学 - 【公示信息表-扫描版】环境学院_0.jpg"



with open(office_path, 'r', encoding='utf8') as file:
    result_num = 0
    i = 0

    image = Image.open(path_1)
    draw = ImageDraw.Draw(image)

    a_1 = 0
    a_2 = 0
    a_3 = 0
    a_4 = 0
    a_5 = 0
    a_6 = 0
    a_7 = 0

    while True:
        lines = file.readline()
        if not lines:
            break
        i += 1
        print(i)
        name = re.search('(.*?).pdf', lines)  # use name.group() to get address of file
        if not name:
            name = re.search('(.*?).jpg', lines)  # some pdf are too large to recognize so i charged to image
        infor = re.search('{(.*)}', lines)
        infor_dict = ast.literal_eval(infor.group())  # infor_dict contains the information of pdf
        result_num += infor_dict['results_num']

        r_1 = re.compile('成果名称')
        r_2 = re.compile('成果完成人')
        r_3 = re.compile('成果完成')
        r_4 = re.compile('单位')
        r_5 = re.compile('第一完成人是否为现任学校领导')
        r_6 = re.compile('是否曾获得过省级及以上教学成果奖')
        r_7 = re.compile('成果简介')
        r_8 = re.compile('申报学校')
        r_9 = re.compile('名称')

        for j in range(infor_dict['results_num']):
            location = infor_dict['results'][j]['words']['words_location']
            left_x = location['left']
            left_y = location['top']
            right_x = location['left'] + location['width']
            right_y = location['top'] + location['height']

            element = infor_dict['results'][j]['words']
            if len(re.findall(r_1, element['word'])) > 0:
                a_1 += 1
                draw.rectangle([left_x, left_y, right_x, right_y], outline=(255, 0, 0), width=1)
                continue
            if len(re.findall(r_2, element['word'])) > 0:
                a_2 += 1
                draw.rectangle([left_x, left_y, right_x, right_y], outline=(0, 255, 0), width=1)
                continue
            elif len(re.findall(r_3, element['word'])) > 0:
                a_3 += 1
                draw.rectangle([left_x, left_y, right_x, right_y], outline=(0, 0, 255), width=1)
                continue
            if len(re.findall(r_5, element['word'])) > 0:
                a_5 += 1
                draw.rectangle([left_x, left_y, right_x, right_y], outline=(0, 255, 255), width=1)
                continue
            if len(re.findall(r_6, element['word'])) > 0:
                a_6 += 1
                draw.rectangle([left_x, left_y, right_x, right_y], outline=(255, 255, 0), width=1)
                continue
            if len(re.findall(r_7, element['word'])) > 0:
                a_7 += 1
                draw.rectangle([left_x, left_y, right_x, right_y], outline=(255, 0, 255), width=1)
                continue
            if len(re.findall(r_8, element['word'])) > 0:
                a_4 += 1
                draw.rectangle([left_x, left_y, right_x, right_y], outline=(128, 128, 128), width=1)

    image.show()
    print("成果名称: " + str(a_1))
    print("成果完成人: " + str(a_2))
    print("成果完成单位: " + str(a_3))
    print("申报学校名称: " + str(a_4))
    print("第一完成人是否为现任学校领导: " + str(a_5))
    print("是否曾获得过省级及以上教学成果奖: " + str(a_6))
    print("成果简介: " + str(a_7))
