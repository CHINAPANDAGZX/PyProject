#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cv2
# capture = cv2.VideoCapture(0)
# while(True):
#     # 获取一帧
#     ret, frame = capture.read()
#     # 将这帧转换为灰度图
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cv2.imshow('frame', gray)
#     if cv2.waitKey(1) == ord('q'):
#         cv2.imwrite("youtemp.png", frame)
#         capture.release() #释放摄像头
#         cv2.destroyAllWindows()#删除建立的全部窗口
#         break

# cap = cv2.VideoCapture(0)
# i = 0
# while (1):
#     ret, frame = cap.read()
#     k = cv2.waitKey(1)
#     if k == 27:
#         break
#     elif k == ord('s'):
#         # cv2.imwrite('d:/' + str(i) + '.jpg', frame)
#         cv2.imwrite('/home/pi/' + str(i) + '.jpg', frame)
#         i += 1
#     cv2.imshow("capture", frame)
# cap.release()
# cv2.destroyAllWindows()


cap = cv2.VideoCapture(0)
i = 0
ret, frame = cap.read()
cv2.imwrite('/home/pi/' + str(i) + '.jpg', frame)
cap.release()
