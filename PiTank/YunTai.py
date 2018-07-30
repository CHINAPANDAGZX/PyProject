#!/usr/bin/python
# -*- coding:utf-8 -*-
############################
#
############################

from Raspi_PWM_Servo_Driver import PWM
import time

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x6F)

# ===========================================================================
# YunTai DuoJi
# ===========================================================================


pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
#
servoMin1 = 300 # Min pulse length out of 4096
servoMid1 = 375
servoMax1 = 630  # Max pulse length out of 4096
#此为俯仰舵机的角度参数
servoMin = 220 # Min pulse length out of 4096
servoMid = 380
servoMax = 630  # Max pulse length out of 4096


def setServoPulse(channel, pulse):
    pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 60                       # 60 Hz
    print "%d us per period" % pulseLength
    pulseLength /= 4096                     # 12 bits of resolution
    print "%d us per bit" % pulseLength
    pulse *= 1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)
def ServoUpdate(channel,pulse):
    pwm.setPWM(channel,0,pulse)


while (True):
  # Change speed of continuous servo on channel O
    #pwm.setPWM(1, 0, servoMin)
    #time.sleep(1)
    #pwm.setPWM(1, 0, servoMax)
    time.sleep(2)
    ServoUpdate(1,servoMax)
    print "max"
    time.sleep(2)
    ServoUpdate(1,servoMin)
    print "min"
    time.sleep(2)
    ServoUpdate(1,servoMid)
    print "mid"
    """pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 50                       # 50 Hz
    print "%d us per period" % pulseLength
    pulseLength /= 4096                     # 12 bits of resolution
    print "%d us per bit" % pulseLength
    pwm.setPWM(0, 0, 108)
    time.sleep(10)"""





