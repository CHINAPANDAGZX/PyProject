import cv2
import numpy as np
import os

cap = cv2.VideoCapture(0)
#capWebcam.set(cv2.CAP_PROP_FRAME_WIDTH, 320.0)              # change resolution to 320x240 for faster processing
#capWebcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240.0)

while(True):
    
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #img = cv2.medianBlur(frame,5)
    #cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    #circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=20)

    #circles = np.uint16(np.around(circles))
    #for i in circles [0,:]:
            #cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            #cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('hh',gray)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
cap.release()
cv2.destoryAllWindows()
