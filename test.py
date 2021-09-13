import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage import io
from skimage.transform import hough_line, hough_line_peaks
from matplotlib import cm

path = "D:\\phthon专用\\20210901\\pdf_new\\99 南京大学 - 【公示信息表-扫描版】环境学院_0.jpg"
new_path = "D:\\phthon专用\\20210901\\pdf_new\\test.jpg"

img = io.imread(new_path)
t = np.mean(img)
tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360, endpoint=False)
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

for _, angle, dist in zip(*hough_line_peaks(h, theta, d, min_distance=50, min_angle=80, num_peaks=14)):
    (x0, y0) = dist * np.array([np.cos(angle), np.sin(angle)])
    plt.axline((x0, y0), slope=np.tan(angle + np.pi/2))
    plt.scatter(x0, y0, s=50, c="red")

plt.tight_layout()
plt.show()
