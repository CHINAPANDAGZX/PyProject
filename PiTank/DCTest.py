#!/usr/bin/python
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
myMotorL = mh.getMotor(1)
myMotorR = mh.getMotor(2)

# set the speed to start, from 0 (off) to 255 (max speed)
#myMotor.setSpeed(150)
#myMotor.run(Raspi_MotorHAT.FORWARD);
# turn on motor
#myMotor.run(Raspi_MotorHAT.RELEASE);
j= 1

while (j<5):
        print "Forward! "
        myMotorL.run(Raspi_MotorHAT.FORWARD)
        myMotorR.run(Raspi_MotorHAT.BACKWARD)
        #myMotorL.setSpeed(200)
        #myMotorR.setSpeed(200)
        #time.sleep(30)
        #myMotorL.setSpeed(0)
        #myMotorR.setSpeed(0)
                
        print "\tSpeed up..."
        for i in range(255):
                myMotorL.setSpeed(i)
                myMotorR.setSpeed(i)
                time.sleep(0.01)

        print "\tSlow down..."
        for i in reversed(range(255)):
                myMotorL.setSpeed(i)
                myMotorR.setSpeed(i)
                time.sleep(0.01)
                
	"""print "Backward! "
	myMotor.run(Raspi_MotorHAT.BACKWARD)

	print "\tSpeed up..."
                 for i in range(255):
		myMotor.setSpeed(i)
		time.sleep(0.01)

	print "\tSlow down..."
	for i in reversed(range(255)):
		myMotor.setSpeed(i)
		time.sleep(0.01)"""

        print "Release"
        myMotorL.run(Raspi_MotorHAT.RELEASE)
        myMotorR.run(Raspi_MotorHAT.RELEASE)
        time.sleep(1.0)
        j= j + 1
        print  j
