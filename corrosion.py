# coding: utf-8
from skimage import morphology
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.transform import hough_line, hough_line_peaks
from matplotlib import cm

path = "D:\\phthon专用\\20210901\\pdf_new\\test.jpg"

img = io.imread(path)

kernel = morphology.rectangle(5, 10)  # vertical use (10, 5), horizon use(5, 10)

img = morphology.erosion(img, kernel)
img = morphology.dilation(img, kernel)
kernel = morphology.rectangle(1, 100)  # remember alter this place
img = morphology.erosion(img, kernel)
img = morphology.dilation(img, kernel)

tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360)
h, theta, d = hough_line(img, theta=tested_angles)

fig, axes = plt.subplots(1, 3, figsize=(15, 6))
ax = axes.ravel()

ax[0].imshow(img, cmap=cm.gray)
ax[0].set_title("original photo")
ax[0].set_axis_off()

angle_step = 0.5 * np.diff(theta).mean()
d_step = 0.5 * np.diff(d).mean()
bounds = [np.rad2deg(theta[0] - angle_step),
          np.rad2deg(theta[-1] + angle_step),
          d[-1] + d_step, d[0] - d_step]

ax[1].imshow(np.log(1 + h), extent=bounds, cmap=cm.gray, aspect='auto')
ax[1].set_title('Hough transform')
ax[1].set_xlabel('Angles (degrees)')
ax[1].set_ylabel('Distance (pixels)')
# ax[1].axis('image')

ax[2].imshow(img, cmap=cm.gray)
ax[2].set_ylim((img.shape[0], 0))
ax[2].set_axis_off()
ax[2].set_title('Detected lines')


i = 0
for _, angle, dist in zip(*hough_line_peaks(h, theta, d, min_distance=100, num_peaks=8)):
    # if detect vertical line, use para(h, theta, d, min_distance=100, threshold=0.2*h.max(), num_peaks=5)
    # if detect horizon line, use para(h, theta, d, min_distance=100, num_peaks=8)
    # for reference only
    i += 1
    (x0, y0) = dist * np.array([np.cos(angle), np.sin(angle)])
    print(x0, y0)
    plt.axline((x0, y0), slope=np.tan(angle + np.pi/2))
    plt.scatter(x0, y0, s=50, c="red")

print(i)
plt.tight_layout()
plt.show()
plt.clf()
plt.imshow(img, cmap=cm.gray)
infor =  {'results_num': 43, 'results': [{'words': {'word': '江苏省教学成果奖(高等教育类)报公示信息表', 'words_location': {'left': 390, 'height': 82, 'width': 1745, 'top': 492}}, 'words_type': 'print'}, {'words': {'word': '成果名称', 'words_location': {'left': 328, 'height': 61, 'width': 246, 'top': 694}}, 'words_type': 'print'}, {'words': {'word': '平台群支撑条赋能:供给割改革视角下环境类工科人才培养探索与实践', 'words_location': {'left': 643, 'height': 44, 'width': 1478, 'top': 718}}, 'words_type': 'print'}, {'words': {'word': '毕军、任洪强,袁增伟、柏益尧、周媛、谷成,杨柳燕、刘建萍、孕梅、刘蓓', 'words_location': {'left': 629, 'height': 51, 'width': 1536, 'top': 838}}, 'words_type': 'print'}, {'words': {'word': '成果完成人', 'words_location': {'left': 297, 'height': 65, 'width': 311, 'top': 876}}, 'words_type': 'print'}, {'words': {'word': '蓓、周庆、顾雪元,孙平', 'words_location': {'left': 1142, 'height': 47, 'width': 643, 'top': 930}}, 'words_type': 'print'}, {'words': {'word': '成果完成', 'words_location': {'left': 325, 'height': 65, 'width': 246, 'top': 1160}}, 'words_type': 'print'}, {'words': {'word': '申报学校', 'words_location': {'left': 1317, 'height': 65, 'width': 253, 'top': 1163}}, 'words_type': 'print'}, {'words': {'word': '南京大学', 'words_location': {'left': 855, 'height': 44, 'width': 174, 'top': 1221}}, 'words_type': 'print'}, {'words': {'word': '南京大学', 'words_location': {'left': 1793, 'height': 41, 'width': 174, 'top': 1221}}, 'words_type': 'print'}, {'words': {'word': '单位', 'words_location': {'left': 390, 'height': 58, 'width': 116, 'top': 1248}}, 'words_type': 'print'}, {'words': {'word': '名称', 'words_location': {'left': 1375, 'height': 65, 'width': 126, 'top': 1245}}, 'words_type': 'print'}, {'words': {'word': '第一完成人是否为现任学校领导(如', 'words_location': {'left': 284, 'height': 61, 'width': 958, 'top': 1491}}, 'words_type': 'print'}, {'words': {'word': '不是请填“否”,如是请填写具体职务', 'words_location': {'left': 277, 'height': 68, 'width': 985, 'top': 1567}}, 'words_type': 'print'}, {'words': {'word': '否', 'words_location': {'left': 1693, 'height': 41, 'width': 47, 'top': 1550}}, 'words_type': 'print'}, {'words': {'word': '是否曾获得过省级及以上教学成果奖', 'words_location': {'left': 280, 'height': 65, 'width': 964, 'top': 1704}}, 'words_type': 'print'}, {'words': {'word': '(未获得请填“否”,曾获得请填写获', 'words_location': {'left': 307, 'height': 61, 'width': 964, 'top': 1779}}, 'words_type': 'print'}, {'words': {'word': '奖时间、授奖部门及奖级)', 'words_location': {'left': 277, 'height': 65, 'width': 698, 'top': 1858}}, 'words_type': 'print'}, {'words': {'word': '成果围绕研究型大学环境类专业在工科人才培养过程中供给侧存在的不', 'words_location': {'left': 715, 'height': 47, 'width': 1430, 'top': 1971}}, 'words_type': 'print'}, {'words': {'word': '足,以顶天立地式人才培养为目标,在南京大学环境学院开展了系列育人改革', 'words_location': {'left': 622, 'height': 47, 'width': 1526, 'top': 2056}}, 'words_type': 'print'}, {'words': {'word': '打造了“教学实验一科技创新一国际交流一社会服务”的全方位育人平台,以此为', 'words_location': {'left': 619, 'height': 44, 'width': 1536, 'top': 2142}}, 'words_type': 'print'}, {'words': {'word': '依托,构建了导师钰课程链、项目链三大路径,通过递进式赋能过程设计,', 'words_location': {'left': 622, 'height': 47, 'width': 1495, 'top': 2227}}, 'words_type': 'print'}, {'words': {'word': '成果简介', 'words_location': {'left': 304, 'height': 71, 'width': 284, 'top': 2268}}, 'words_type': 'print'}, {'words': {'word': '满足了学生在大学不同成长时期的差异化能量需求:实现了全员全过程育人。', 'words_location': {'left': 619, 'height': 47, 'width': 1505, 'top': 2309}}, 'words_type': 'print'}, {'words': {'word': '(300字内', 'words_location': {'left': 304, 'height': 47, 'width': 301, 'top': 2374}}, 'words_type': 'print'}, {'words': {'word': '充分发挥平台与赋能链在人才培养过程中的积极作用,逐步完善了基于“价值', 'words_location': {'left': 619, 'height': 47, 'width': 1533, 'top': 2395}}, 'words_type': 'print'}, {'words': {'word': '融合知识融合实践融合”培养理念的育人体系建设,成果成功打道了学科', 'words_location': {'left': 615, 'height': 51, 'width': 1536, 'top': 2477}}, 'words_type': 'print'}, {'words': {'word': '发展优势向教育教学资源持续转化的新路径,支撑了研究型大学环境类新工科', 'words_location': {'left': 615, 'height': 47, 'width': 1526, 'top': 2562}}, 'words_type': 'print'}, {'words': {'word': '人才培养过程与目标的有力衔接,在专业领域得到了广泛认可。', 'words_location': {'left': 622, 'height': 47, 'width': 1235, 'top': 2648}}, 'words_type': 'print'}, {'words': {'word': '南京大学环境学院:', 'words_location': {'left': 1197, 'height': 47, 'width': 372, 'top': 2734}}, 'words_type': 'print'}, {'words': {'word': '专业技术', 'words_location': {'left': 1659, 'height': 44, 'width': 177, 'top': 2737}}, 'words_type': 'print'}, {'words': {'word': '姓名', 'words_location': {'left': 482, 'height': 44, 'width': 106, 'top': 2775}}, 'words_type': 'print'}, {'words': {'word': '毕军', 'words_location': {'left': 701, 'height': 37, 'width': 109, 'top': 2775}}, 'words_type': 'print'}, {'words': {'word': '单位及职务', 'words_location': {'left': 920, 'height': 44, 'width': 208, 'top': 2775}}, 'words_type': 'print'}, {'words': {'word': '主要完成', 'words_location': {'left': 284, 'height': 273, 'width': 65, 'top': 2775}}, 'words_type': 'print'}, {'words': {'word': '国家重点实验室主任', 'words_location': {'left': 1197, 'height': 47, 'width': 417, 'top': 2792}}, 'words_type': 'print'}, {'words': {'word': '职称', 'words_location': {'left': 1700, 'height': 37, 'width': 102, 'top': 2792}}, 'words_type': 'print'}, {'words': {'word': '教授', 'words_location': {'left': 1971, 'height': 41, 'width': 92, 'top': 2778}}, 'words_type': 'print'}, {'words': {'word': '三持成果的方案设计诊证和实施:完善环境学院本科生管理制度;牵头推动', 'words_location': {'left': 619, 'height': 47, 'width': 1522, 'top': 2894}}, 'words_type': 'print'}, {'words': {'word': '主安', 'words_location': {'left': 485, 'height': 92, 'width': 102, 'top': 2935}}, 'words_type': 'print'}, {'words': {'word': '贡献', 'words_location': {'left': 485, 'height': 95, 'width': 106, 'top': 2963}}, 'words_type': 'print'}, {'words': {'word': '环境科学与工程国家级实验教学中心等平台的成立;作为学校环境校友会首届', 'words_location': {'left': 612, 'height': 47, 'width': 1526, 'top': 2977}}, 'words_type': 'print'}, {'words': {'word': '会长搭建优秀校友资源的反哺渠道;培养出国家杰青等优秀人才30余位。', 'words_location': {'left': 619, 'height': 51, 'width': 1447, 'top': 3059}}, 'words_type': 'print'}], 'log_id': 1435973406397948186}
for j in range(infor['results_num']):
    location = infor['results'][j]['words']['words_location']
    left_x = location['left']
    left_y = location['top']
    width = location['width']
    height = location['height']
    plt.gca().add_patch(plt.Rectangle((left_x, left_y), width, height))
plt.show()
