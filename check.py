import os_operate
import requests
from bs4 import BeautifulSoup
import re

Path = []
Filename = []
for j in range(27):
    target = "https://jsgjc.jse.edu.cn/jxcg/WSGS?PageIndex=" + str(j + 1)
    req = requests.get(url=target)
    html = req.text
    bs = BeautifulSoup(html)
    div = bs.find_all('div', class_="hidden td-data")
    length = len(div)


    School = []
    header = "https://jsgjc.jse.edu.cn/jxcg/"

    td = bs.find_all('td')
    for i in range(len(td)):
        text = str(td[i])
        s = re.search(r'<td>\r\n(.*?)\r\n', text)
        if s:
            source = s.group(1).strip()
            School.append(source)

    for i in range(length):
        line = str(div[i])
        path = re.search('data-name="FilePath" data-value="(.*?)"', line)
        Path.append(header + path.group(1))
        Filename.append(School[2 * i])

print(len(Filename))