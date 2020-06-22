# -*- coding:utf-8 -*-

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# cap.set = (cv2.CAP_PROP_FRAME_WIDTH,1280)
# cap.set = (cv2.CAP_PROP_FRAME_HEIGHT,480)

low_white = np.array([0, 20, 46])
high_white = np.array([10, 100, 255])

while (1):
    ret, frame = cap.read()
    # img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # img = cv2.medianBlur(img, 5)
    # ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    Gbframe = cv2.GaussianBlur(hsvframe, (5, 5), 0)

    mask = cv2.inRange(hsvframe, low_white, high_white)
    res = cv2.bitwise_and(Gbframe, Gbframe, mask=mask)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret, th1 = cv2.threshold(res, 120, 255, cv2.THRESH_BINARY)  # 颜色过滤

    kernel = np.ones((11, 11), np.uint8)
    erosion = cv2.erode(th1, kernel)
    dilation = cv2.dilate(erosion, kernel)  # 腐蚀膨胀

    # cv2.imshow("th2", th1)
    cv2.imshow("dilation", dilation)
    th2 = th1

    # th2 = cv2.adaptiveThreshold(res, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    image, contours, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, 0, (255, 0, 0), 3)  # 轮廓检测与显示
    if contours == []:
        pass
    else:
        cnt = contours[0]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绘制轮廓
        M = cv2.moments(cnt)
        # print M
        if M['m00'] != 0:  # 此处防止除数为零导致错误
            mx = int(M['m10'] / M['m00'])
            my = int(M['m01'] / M['m00'])
            cv2.circle(frame, (mx, my), 5, (0, 0, 255), -1)  # 红点标示重心
            zx = int(mx + (w / 2) * 1.5)
            zy = int(my - (h / 2) * 1.5)
            zx2 = int(zx + (w / 2))
            zy2 = zy
            frame = cv2.line(frame, (mx, my), (zx, zy), (0, 255, 0), 3)
            frame = cv2.line(frame, (zx, zy), (zx2, zy2), (0, 255, 0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'Target', (zx2 + 1, zy2 + 2), font, 0.5, (255, 255, 255), 1)

    cv2.imshow("frame", frame)
    # cv2.imshow("th2", th1)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
