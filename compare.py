import os
import re
import ast

office_path = "picture.txt"
accurate_path = "高精度含位置.txt"
general_path = "general.txt"



# 标准含位置
with open(general_path, 'r', encoding='utf8') as file:
    result_num = 0
    i = 0
    while True:
        lines = file.readline()
        if not lines:
            break
        i += 1
        name = re.search('(.*?).pdf', lines)  # use name.group() to get address of pdf
        infor = re.search('{(.*)}', lines)
        infor_dict = ast.literal_eval(infor.group())  # infor_dict contains the information of pdf
        result_num += infor_dict['words_result_num']

    print("general ORC: (has " + str(i) + " files)")
    print("average words number: " + str(result_num / i))

# 高精度含位置
with open(accurate_path, 'r', encoding='utf8') as file:
    result_num = 0
    i = 0
    while True:
        lines = file.readline()
        if not lines:
            break
        i += 1
        name = re.search('(.*?).pdf', lines)  # use name.group() to get address of pdf
        infor = re.search('{(.*)}', lines)
        infor_dict = ast.literal_eval(infor.group())  # infor_dict contains the information of pdf
        result_num += infor_dict['words_result_num']

    print("accurate ORC: (has " + str(i) + " files)")
    print("average words number: " + str(result_num / i))

# 办公文档
with open(office_path, 'r', encoding='utf8') as file:
    result_num = 0
    i = 0
    while True:
        lines = file.readline()
        if not lines:
            break
        i += 1
        print(i)
        name = re.search('(.*?).jpg', lines)  # use name.group() to get address of pdf
        infor = re.search('{(.*)}', lines)
        infor_dict = ast.literal_eval(infor.group())  # infor_dict contains the information of pdf
        result_num += infor_dict['results_num']

    print("office ORC: (has " + str(i) + " files)")
    print("average words number: " + str(result_num / i))