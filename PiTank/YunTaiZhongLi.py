#!/usr/bin/python
#-*- coding:utf-8 -*
from Raspi_PWM_Servo_Driver import PWM
import time
import cv2

pwm = PWM(0x6F)
servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

cap = cv2.VideoCapture(0)

while(True):
        ret,frame = cap.read()
        KeyCode =  cv2.waitKey(1)
        KeyCode &= 0xFF
        cv2.imshow("capture",frame)
        if KeyCode == ord('i'):#up
                pwm.setPWM(0,0,600)
                pwm.setPWM(1,0,370)
                print "云台抬起!"
                
        if KeyCode == ord('k'):#mid
                pwm.setPWM(0,0,390)
                pwm.setPWM(1,0,370)
                print "云台中立位!"
                
        if KeyCode == ord('m'):#down
                pwm.setPWM(0,0,210)
                pwm.setPWM(1,0,370)
                print "云台收!"
        if KeyCode == ord('l'):#right
                pwm.setPWM(0,0,390)
                pwm.setPWM(1,0,250)
                print "云台右转最大!"
        if KeyCode == ord('j'):#left
                pwm.setPWM(0,0,390)
                pwm.setPWM(1,0,490)
                print "云台左转最大!"
	if KeyCode == ord('c'):                
		cap.release()
		cv2.destroyAllWindows()
        
