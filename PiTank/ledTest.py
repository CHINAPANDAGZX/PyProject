#!/usr/bin/python
# -*- coding:utf-8 -*-
############################
#
############################

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(35,GPIO.OUT)

start_time  = time.time()
for i in range(0,1000000):
        GPIO.output(35,1)
        pass

end_time = time.time()

print(end_time - start_time)
GPIO.cleanup()
