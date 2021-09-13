# coding: utf-8
from PIL import Image
from skimage import morphology
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.transform import hough_line, hough_line_peaks
from matplotlib import cm
import re
import pandas as pd
import ast

def judgement(specified_end1, specified_end2, object_end1, object_end2):
    # specified_endpoint 指正确的表格位置，object_endpoint 指识别文字的位置
    # 该函数检测识别文字是否在正确的表格位置中，其中含有参数3/4，保证留有一定的缓冲空间
    a1 = specified_end1 if specified_end1 < specified_end2 else specified_end2
    a2 = specified_end2 if specified_end1 < specified_end2 else specified_end1
    b1 = object_end1 if object_end1 < object_end2 else object_end2
    b2 = object_end2 if object_end1 < object_end2 else object_end1
    if a1 < b1 and a2 > b2:
        return True
    c = min(b2-a1, a2-b1)
    if c > 3 / 4 * (b2 - b1):
        return True
    else:
        return False

def intersort(l):
    # 简简单单的一个选择排序
    for c in range(len(l)):
        min_idx = c
        for j in range(c + 1, len(l)):
            if l[min_idx] > l[j]:
                min_idx = j
        l[c], l[min_idx] = l[min_idx], l[c]

def pd_toExcel(data, fileName):
    # pandas库储存数据到excel
    a_1 = []
    a_2 = []
    a_3 = []
    a_4 = []
    a_5 = []
    a_6 = []
    a_7 = []
    a_8 = []

    for n in range(len(data)):
        a_1.append(data[n]["成果名称"])
        a_2.append(data[n]["成果完成人"])
        a_3.append(data[n]["成果完成单位"])
        a_4.append(data[n]["申报学校名称"])
        a_5.append(data[n]["第一完成人是否为现任学校领导"])
        a_6.append(data[n]["是否曾获得过省级及以上教学成果奖"])
        a_7.append(data[n]["成果简介"])
        a_8.append(data[n]["path"])

    dfData = {  # 用字典设置DataFrame所需数据
        "path": a_8,
        "成果名称": a_1,
        "成果完成人": a_2,
        "成果完成单位": a_3,
        "申报学校名称": a_4,
        "第一完成人是否为现任学校领导": a_5,
        "是否曾获得过省级及以上教学成果奖": a_6,
        "成果简介": a_7
    }
    df = pd.DataFrame(dfData)  # 创建DataFrame
    df.to_excel(fileName, index=False)  # 存表，去除原始索引列（0,1,2...）


office_path = "picture.txt"  # OCR文档地址，在第二次运行程序时改为日志文档地址
path = "D:\\phthon专用\\20210901\\PDF\\"  # 图片存放地址

data_total = []

ii = 0
with open(office_path, 'r', encoding='utf8') as file:
    while True:
        ii += 1
        lines = file.readline()
        if not lines:
            break
        name = re.search('(.*?).jpg', lines)  # 使用 name.group() 获取图片名称
        infor = re.search('{(.*)}', lines)
        infor_dict = ast.literal_eval(infor.group())  # infor_dict 包含OCR内容识别的信息，格式为字典

        img = io.imread(path + name.group())  # 读取图片

        # 和plt有关的部分均为可视化形态学操作的结果，用于人工判断问题所在，可注释掉以确保代码的执行效率
        fig, axes = plt.subplots(1, 3, figsize=(15, 6))
        ax = axes.ravel()
        ax[0].imshow(img, cmap=cm.gray)

        # 纵向检测
        kernel = morphology.rectangle(2, 10)  # 纵向算子使用参数 (10, 5), 横向使用参数 (5, 10), 不过意义不大，还需要自己调试
        img_horizon = morphology.erosion(img, kernel)
        img_horizon = morphology.dilation(img_horizon, kernel)

        kernel = morphology.rectangle(1, 100)  # 二次腐蚀膨胀操作，需修改算子，不要忘记和第一个保持方向一致
        img_horizon = morphology.erosion(img_horizon, kernel)
        img_horizon = morphology.dilation(img_horizon, kernel)

        tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360)
        h, theta, d = hough_line(img_horizon, theta=tested_angles)  # 霍夫变换

        ax[1].imshow(img_horizon, cmap=cm.gray)
        horizon_point = []
        for _, angle, dist in zip(*hough_line_peaks(h, theta, d, min_distance=30, threshold=0.1*h.max(), num_peaks=12)):
            # if detect vertical line, use para(h, theta, d, min_distance=100, threshold=0.2*h.max(), num_peaks=5)
            # if detect horizon line, use para(h, theta, d, min_distance=100, num_peaks=8)
            # 上述参数均为调整所得，仅供参考
            # for reference only
            (x0, y0) = dist * np.array([np.cos(angle), np.sin(angle)])
            if y0 < 50:
                continue
            horizon_point.append(y0)
            ax[1].axline((x0, y0), slope=np.tan(angle + np.pi / 2))
        intersort(horizon_point)

        # 横向检测
        kernel = morphology.rectangle(7, 2)  # vertical use (10, 5), horizon use(5, 10)， 同上
        img_vertical = morphology.erosion(img, kernel)
        img_vertical = morphology.dilation(img_vertical, kernel)

        kernel = morphology.rectangle(50, 1)  # remember alter this place
        img_vertical = morphology.erosion(img_vertical, kernel)
        img_vertical = morphology.dilation(img_vertical, kernel)
        ax[2].imshow(img_vertical, cmap=cm.gray)

        tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360)
        h, theta, d = hough_line(img_vertical, theta=tested_angles)

        vertical_point = []
        for _, angle, dist in zip(*hough_line_peaks(h, theta, d, min_distance=200, threshold=0.1*h.max(), num_peaks=5)):
            # if detect vertical line, use para(h, theta, d, min_distance=100, threshold=0.2*h.max(), num_peaks=5)
            # if detect horizon line, use para(h, theta, d, min_distance=100, num_peaks=8)
            # for reference only
            (x0, y0) = dist * np.array([np.cos(angle), np.sin(angle)])
            if x0 < 100:
                continue
            ax[2].axline((x0, y0), slope=np.tan(angle + np.pi / 2))
            vertical_point.append(x0)
        intersort(vertical_point)
        if len(vertical_point) == 4:
            # 由于第四条线较短，比较难以识别，但又比较重要，发现3，4条线的距离和1，2条线的距离相近，所以如果未能识别，则用其进行代替
            vertical_point.insert(3, vertical_point[2] + vertical_point[1] - vertical_point[0])

        if len(vertical_point) < 5 or len(horizon_point) < 7:
            # 经过横向纵向检测后，判断所识别的线条是否达到要求
            with open("log.txt", "a", encoding="utf8") as f:
                f.write(str(path + name.group()) + " " + infor.group() + "\n")
            print("this file fail to read: cause points too little", end=' ')
            print(path + name.group())
            continue

        r_1 = re.compile('名称')
        r_2 = re.compile('是否为现任学校')
        r_3 = re.compile('申报学')
        t = 0

        data = {"成果名称": "", "成果完成人": "", "成果完成单位": "", "申报学校名称": "", "第一完成人是否为现任学校领导": "",
                "是否曾获得过省级及以上教学成果奖": "", "成果简介": "", "path": name.group()}
        p = 1
        for k in range(2):
            # 分两次循环，第一次检测位置，第二次判断内容并保存
            for i in range(infor_dict['results_num']):
                element = infor_dict['results'][i]['words']
                location = element['words_location']
                left_x = location['left']
                left_y = location['top']
                width = location['width']
                height = location['height']
                if t < 16:
                    # 第一次识别，若报错返回t数值，则可以根据返回的t值来判断哪些直线检测未通过
                    if len(re.findall(r_1, element['word'])) > 0 and t == 0:
                        if judgement(horizon_point[0 + p], horizon_point[1 + p], left_y, left_y + height):
                            t += 1
                        if judgement(vertical_point[0], vertical_point[1], left_x, left_x + width):
                            t += 3
                    if len(re.findall(r_2, element['word'])) > 0:
                        if judgement(horizon_point[3 + p], horizon_point[4 + p], left_y, left_y + height):
                            t += 5
                    if len(re.findall(r_3, element['word'])) > 0:
                        if judgement(vertical_point[2], vertical_point[3], left_x, left_x + width):
                            t += 7
                if t == 16:
                    t += 1
                    break
                if t > 16:
                    # 第二次识别，根据位置写入相应的内容至列表，最后统一写入execl
                    if judgement(horizon_point[0 + p], horizon_point[1 + p], left_y, left_y + height) and judgement(vertical_point[1], vertical_point[4], left_x, left_x + width):
                        data["成果名称"] += element['word']
                        continue
                    if judgement(horizon_point[1 + p], horizon_point[2 + p], left_y, left_y + height) and judgement(vertical_point[1], vertical_point[4], left_x, left_x + width):
                        data["成果完成人"] += element['word']
                        continue
                    if judgement(horizon_point[2 + p], horizon_point[3 + p], left_y, left_y + height) and judgement(vertical_point[1], vertical_point[2], left_x, left_x + width):
                        data["成果完成单位"] += element['word']
                        continue
                    if judgement(horizon_point[2 + p], horizon_point[3 + p], left_y, left_y + height) and judgement(vertical_point[3], vertical_point[4], left_x, left_x + width):
                        data["申报学校名称"] += element['word']
                        continue
                    if judgement(horizon_point[3 + p], horizon_point[4 + p], left_y, left_y + height) and judgement(vertical_point[2], vertical_point[4], left_x, left_x + width):
                        data["第一完成人是否为现任学校领导"] += element['word']
                        continue
                    if judgement(horizon_point[4 + p], horizon_point[5 + p], left_y, left_y + height) and judgement(vertical_point[2], vertical_point[4], left_x, left_x + width):
                        data["是否曾获得过省级及以上教学成果奖"] += element['word']
                        continue
                    if judgement(horizon_point[5 + p], horizon_point[6 + p], left_y, left_y + height) and judgement(vertical_point[1], vertical_point[4], left_x, left_x + width):
                        data["成果简介"] += element['word']

            if t < 16:
                # 返回错误类型，并写入文档
                with open("log.txt", "a", encoding="utf8") as f:
                    f.write(str(path + name.group()) + " " + infor.group() + "\n")
                print("this file fail to read: error number:" + str(16 - t), end=' ')
                print(path + name.group())
                break
        data_total.append(data)
        print(ii)

        plt.show()  # 用于展示形态学操作所检测到的线条，不用时可以注释掉

pd_toExcel(data_total, "test_4.xlsx")  # 写入execl操作

