"""
识别仪表盘度数实验代码
时间：2022年11月14日15:27:16
"""

import cv2

img = cv2.imread('meter.jpg', cv2.IMREAD_GRAYSCALE)
# cv2.line()接受以下参数：图片，开始坐标，结束坐标，颜色（bgr），线条粗细。
cv2.line(img, (0, 0), (150, 150), (255, 255, 255), 15)
cv2.imshow('meter', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
