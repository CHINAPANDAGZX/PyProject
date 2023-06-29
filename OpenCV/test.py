#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cv2
import numpy as np
from matplotlib import pyplot as plt

"""
纯OpenCV实现方式
"""
# img = cv2.imread('watch.jpg', cv2.IMREAD_GRAYSCALE)
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


"""
使用Matplotlib实现方式
"""
img = cv2.imread('watch.jpg',cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.plot([200,300,400],[100,200,300],'c', linewidth=5)
plt.show()
