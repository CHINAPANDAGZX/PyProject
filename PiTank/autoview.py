#!/usr/bin/python
# -*- coding:utf-8 -*-
############################
#云台追踪优化
############################

from Raspi_PWM_Servo_Driver import PWM
import time
#RAS-HAT
import cv2
import numpy as np
import os
import sys
from operator import itemgetter
#COMPUTER VIEWSION

global picth 
global yaw
##picth = 90
#yaw = 90


def main():

    capWebcam = cv2.VideoCapture(0)                     # declare a VideoCapture object and associate to webcam, 0 => use 1st webcam

                                                        # show original resolution
    print "default resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    capWebcam.set(cv2.CAP_PROP_FRAME_WIDTH, 320.0)              # change resolution to 320x240 for faster processing
    capWebcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240.0)

                                                        # show updated resolution
    print "updated resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if capWebcam.isOpened() == False:                           # check if VideoCapture object was associated to webcam successfully
        print "error: capWebcam not accessed successfully\n\n"          # if not, print error message to std out
        os.system("pause")                                              # pause until user presses a key so user can see error message
        return                                                          # and exit function (which exits program)
    # end if

    while cv2.waitKey(1) != 27 and capWebcam.isOpened():                # until the Esc key is pressed or webcam connection is lost
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()            # read next frame

        if not blnFrameReadSuccessfully or imgOriginal is None:             # if frame was not read successfully
            print "error: frame not read from webcam\n"                     # print error message to std out
            os.system("pause")                                              # pause until user presses a key so user can see error message
            break                                                           # exit while loop (which exits program)
        # end if

        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

        imgThreshLow = cv2.inRange(imgHSV, np.array([0, 135, 135]), np.array([18, 255, 255]))
        imgThreshHigh = cv2.inRange(imgHSV, np.array([165, 135, 135]), np.array([179, 255, 255]))
        imgThresh = cv2.add(imgThreshLow, imgThreshHigh)
        # 阈值限定
        imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)

        imgThresh = cv2.dilate(imgThresh, np.ones((5,5),np.uint8))
        imgThresh = cv2.erode(imgThresh, np.ones((5,5),np.uint8))

        intRows, intColumns = imgThresh.shape
        #####################################################################################
        # 图像设置处理
        #####################################################################################

        """for circle in circles[0] :  # for each circle
            tx, ty, tradius = circle  # break out x, y, and radius
            #if tradius > radius :     #提取最大圆的参数
                #x,y,radius = circle
            #print "ball position x = " + str(x) + ", y = " + str(y) + ", radius = " + str(radius)  # print ball position and radius

            cv2.circle(imgOriginal, (tx, ty), 3, (0, 255, 0), -1)  # draw small green circle at center of detected object
            cv2.circle(imgOriginal, (tx, ty), tradius, (0, 0, 255), 3)  # draw red circle around the detected object
        # end for"""

        circles = cv2.HoughCircles(imgThresh, cv2.HOUGH_GRADIENT, 5,
                                   intRows / 4)  # fill variable circles with all circles in the processed image
            ####################################
            # locked circle
            ####################################
        picth = 90
        yaw = 90
        if circles is not None:
            # this line is necessary to keep program from crashing on next line if no circles were found
            sortedCircles = sorted(circles[0], key=itemgetter(2), reverse=True)
            # sortedCircles = sorted(e, key=lambda x: x[2], reverse=True)
            largestCircle = sortedCircles[0]
            x, y, radius = largestCircle  # break out x, y, and radius

            print "ball position x = " + str(x) + ", y = " + str(y) + ", radius = " + str(radius)
            # print ball position and radius

            intXFrameCenter = int(float(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) / 2.0)
            intYFrameCenter = int(float(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) / 2.0)
            

            if x < intXFrameCenter - 5 and yaw >= 2:
                yaw = yaw - 2
            elif x > intXFrameCenter + 5 and yaw <= 178:
                yaw = yaw + 2
            # end if else
            if y < intYFrameCenter - 5 and picth >= 62:
                picth = picth - 2
            elif y > intYFrameCenter + 5 and picth <= 132:
                picth = picth + 2
            # end if else
        if circles is None:
            updateServoMotorPositions(90, 90)
            print "No Search Ball"
            #if not



        cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)            # create windows, use WINDOW_AUTOSIZE for a fixed window size
        cv2.namedWindow("imgThresh", cv2.WINDOW_AUTOSIZE)           # or use WINDOW_NORMAL to allow window resizing

        cv2.imshow("imgOriginal", imgOriginal)                 # show windows
        cv2.imshow("imgThresh", imgThresh)
    # end while

    cv2.destroyAllWindows()                     # remove windows from memory

    return
###################################################################################################
def updateServoMotorPositions( picth , yaw ):
    # Initialise the PWM device using the default address
    # bmp = PWM(0x40, debug=True)
    pwm = PWM(0x6F)
    pwm.setPWMFreq(60)  # Set frequency to 60 Hz
    servoMin1 = 150  # Min pulse length out of 4096
    #servoMid = 375  # Min pulse length out of 4096
    servoMax1 = 490  # Max pulse length out of 4096
    servoMin0 = 250  # Min pulse length out of 4096
    #servoMid = 375  # Min pulse length out of 4096
    servoMax0 = 600  # Max pulse length out of 4096
    pulsePerAngle1 = 2.5
    pulsePerAngle0 = 2.5
    pulsePicth = int(250 + (picth-20) *pulsePerAngle0 )  #caculating angle to pulse
    pulseYaw = int(150 + (yaw -2)* pulsePerAngle1)

    pwm.setPWM(0, 0, pulsePicth)   #output to servo
    pwm.setPWM(1, 0, pulseYaw)
# end function

###################################################################################################
if __name__ == "__main__":
    main()

