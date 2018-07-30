#-*- coding:utf-8 -*-
"""用于控制坦克车身部分功能"""
import time
from HAT.Raspi_MotorHAT import Raspi_MotorHAT
from HAT.Raspi_MotorHAT import Raspi_DCMotor
mh = Raspi_MotorHAT(addr=0x6f) #设置控制板的I2C地址为0x6f

myMotorL = mh.getMotor(1)
myMotorR = mh.getMotor(2)
class Tank():
    def __init__(self):
        pass
    #前进，此处的speed是指给电机的PWM值，0-255
    def Forward(self,speed):
        myMotorL.run(Raspi_MotorHAT.FORWARD)
        myMotorR.run(Raspi_MotorHAT.FORWARD)
        myMotorL.setSpeed(speed)
        myMotorR.setSpeed(speed)
        print "Forward! "
    def Backward(self,speed):
        myMotorL.run(Raspi_MotorHAT.BACKWARD)
        myMotorR.run(Raspi_MotorHAT.BACKWARD)
        myMotorL.setSpeed(speed)
        myMotorR.setSpeed(speed)
        print "Backward! "
    #停车，不确定是否会滑行
    def Stop(self):
        myMotorL.run(Raspi_MotorHAT.FORWARD)
        myMotorR.run(Raspi_MotorHAT.FORWARD)
        myMotorL.setSpeed(0)
        myMotorR.setSpeed(0)
        print "Stop!"
    #停车转向
    def TurnLeft_stop(self):
        myMotorL.run(Raspi_MotorHAT.FORWARD)
        myMotorR.run(Raspi_MotorHAT.BACKWARD)
        myMotorL.setSpeed(0)
        myMotorR.setSpeed(150)
        print "TurnLeft_stop!"
    def TurnRight_stop(self):
        myMotorL.run(Raspi_MotorHAT.BACKWARD)
        myMotorR.run(Raspi_MotorHAT.FORWARD)
        myMotorL.setSpeed(150)
        myMotorR.setSpeed(0)
        print "TurnRight_stop!"
    #待完善，行进转向
    def TurnLeft_move(self,speed):
        myMotorL.run(Raspi_MotorHAT.BACKWARD)
        myMotorR.run(Raspi_MotorHAT.BACKWARD)
        myMotorL.setSpeed(speed)
        myMotorR.setSpeed(speed)
    def TurnRight_move(self,speed):
        myMotorL.run(Raspi_MotorHAT.BACKWARD)
        myMotorR.run(Raspi_MotorHAT.BACKWARD)
        myMotorL.setSpeed(speed)
        myMotorR.setSpeed(speed)
    #前大灯
    def Forward_light(self):
        pass
    #后车灯
    def Backward_light(self):
        pass
    #主炮开火
    def BigGunFire(self):
        pass
    #机枪开火
    def GunFire(self):
        pass
    #超声波测距
    def Senor(self):
        pass
    #GPS数据采集
    def GPS(self):
        pass

tank = Tank()
tank.Forward(150)
time.sleep(2)
tank.Backward(150)
time.sleep(2)
tank.Stop()
time.sleep(2)
tank.TurnLeft_stop()
time.sleep(2)
tank.TurnRight_stop()
time.sleep(2)
tank.Stop()
print "test done!"
