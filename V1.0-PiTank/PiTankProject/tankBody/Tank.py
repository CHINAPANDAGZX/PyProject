#!/usr/bin/python
# -*- coding:utf-8 -*-
############################
#用于控制坦克车身部分功能
############################

import time
# 引入GPIO驱动库
import RPi.GPIO as GPIO
# 引入拓展板库
from ..HAT.Raspi_MotorHAT import Raspi_MotorHAT
from ..HAT.Raspi_MotorHAT import Raspi_DCMotor
from ..HAT.Raspi_PWM_Servo_Driver import PWM



class Tank():
    mh = Raspi_MotorHAT(addr=0x6f)  # 设置控制板的I2C地址为0x6f
    pwm = PWM(0x6F) # 意义暂时不明，示例程序中照抄
    pwm.setPWMFreq(60)  # 设置60HZ频率
    myMotorL = mh.getMotor(1)  # 设置电机的接线位置
    myMotorR = mh.getMotor(2)
    # 此为偏航舵机的角度参数
    servoMin_yaw = 300  # Min pulse length out of 4096
    servoMid_yaw = 375
    servoMax_yaw = 630  # Max pulse length out of 4096
    # 此为俯仰舵机的角度参数(60HZ时)
    servoMin_pitch = 220  # Min pulse length out of 4096
    servoMid_pitch = 380
    servoMax_pitch = 630  # Max pulse length out of 4096
    servoYawNum = 0
    servoPitchNum = 1
    def __init__(self):
        pass
    #前进，此处的speed是指给电机的PWM值，0-255
    def Forward(self,speed):
        self.myMotorL.run(Raspi_MotorHAT.FORWARD)
        self.myMotorR.run(Raspi_MotorHAT.FORWARD)
        self.myMotorL.setSpeed(speed)
        self.myMotorR.setSpeed(speed)
        print "坦克前进! "

    #后退
    def Backward(self,speed):
        self.myMotorL.run(Raspi_MotorHAT.BACKWARD)
        self.myMotorR.run(Raspi_MotorHAT.BACKWARD)
        self.myMotorL.setSpeed(speed)
        self.myMotorR.setSpeed(speed)
        print "坦克后退! "
    #停车，不确定是否会滑行
    def Stop(self):
        self.myMotorL.run(Raspi_MotorHAT.FORWARD)
        self.myMotorR.run(Raspi_MotorHAT.FORWARD)
        self.myMotorL.setSpeed(0)
        self.myMotorR.setSpeed(0)
        print "坦克停车!"
    #原地左转向
    def TurnLeft_stop(self):
        self.myMotorL.run(Raspi_MotorHAT.FORWARD)
        self.myMotorR.run(Raspi_MotorHAT.BACKWARD)
        self.myMotorL.setSpeed(0)
        self.myMotorR.setSpeed(150)
        print "坦克左转向!"
    #原地右转向
    def TurnRight_stop(self):
        self.myMotorL.run(Raspi_MotorHAT.BACKWARD)
        self.myMotorR.run(Raspi_MotorHAT.FORWARD)
        self.myMotorL.setSpeed(150)
        self.myMotorR.setSpeed(0)
        print "坦克右转向!"
    #待完善，行进转向
    def TurnLeft_move(self,speed):
        self.myMotorL.run(Raspi_MotorHAT.BACKWARD)
        self.myMotorR.run(Raspi_MotorHAT.BACKWARD)
        self.myMotorL.setSpeed(speed)
        self.myMotorR.setSpeed(speed)
    # 待完善，行进转向
    def TurnRight_move(self,speed):
        self.myMotorL.run(Raspi_MotorHAT.BACKWARD)
        self.myMotorR.run(Raspi_MotorHAT.BACKWARD)
        self.myMotorL.setSpeed(speed)
        self.myMotorR.setSpeed(speed)
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

############################
#测试坦克车体移动函数
############################
def testTankRun():
    '''
    测试坦克车体移动函数
    :return:None
    '''
    print "测试坦克车体————底盘部分开始!"
    tank = Tank()
    print "坦克前进!"
    tank.Forward(150)
    time.sleep(2)
    print "坦克后退!"
    tank.Backward(150)
    time.sleep(2)
    print "坦克停止!"
    tank.Stop()
    time.sleep(2)
    print "坦克原地左转!"
    tank.TurnLeft_stop()
    time.sleep(2)
    print "坦克原地右转!"
    tank.TurnRight_stop()
    time.sleep(2)
    print "坦克停止!"
    tank.Stop()
    print "测试坦克车体————底盘部分结束!"

############################
#测试坦克车灯功能函数
############################
def testTankLight():
    '''
    测试坦克车灯功能函数
    :return:None
    '''
    print '测试坦克车体————车灯部分开始!'
    # 指定GPIO口的选定模式为GPIO引脚编号模式（而非主板编号模式）
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    # 指定GPIO14（就是LED长针连接的GPIO针脚）的模式为输出模式
    # 如果上面GPIO口的选定模式指定为主板模式的话，这里就应该指定8号而不是14号。
    RPi.GPIO.setup(14, RPi.GPIO.OUT)#暂定14，15前车灯
    RPi.GPIO.setup(15, RPi.GPIO.OUT)
    RPi.GPIO.setup(16, RPi.GPIO.OUT)#暂定16，17后车灯
    RPi.GPIO.setup(17, RPi.GPIO.OUT)
    print '前后车灯将于一秒后闪亮五次!'
    time.sleep(1)
    # 循环5次
    for i in range(0, 5):
        # 让GPIO14输出高电平（LED灯亮）
        RPi.GPIO.output(14, True)
        RPi.GPIO.output(15, True)
        RPi.GPIO.output(16, True)
        RPi.GPIO.output(17, True)
        # 持续一段时间
        time.sleep(0.5)
        # 让GPIO14输出低电平（LED灯灭）
        RPi.GPIO.output(14, False)
        RPi.GPIO.output(15, False)
        RPi.GPIO.output(16, False)
        RPi.GPIO.output(17, False)

        # 持续一段时间
        time.sleep(0.5)
    # 最后清理GPIO口（不做也可以，建议每次程序结束时清理一下，好习惯）
    RPi.GPIO.cleanup()
    print '测试坦克车体————车灯部分结束!'

############################
#测试坦克云台功能函数
############################
def testTankPlatform():
    '''
    测试坦克云台功能函数
    :return:None
    '''
    print "测试坦克车体————云台部分开始！"
    tank = Tank()
    print "俯仰云台部分开始！"
    time.sleep(2)
    print "俯仰云台展开！"
    tank.pwm.setPWM(tank.servoPitchNum, 0, tank.servoMid_pitch)
    time.sleep(2)
    print "俯仰云台最大仰角！"
    tank.pwm.setPWM(tank.servoPitchNum, 0, tank.servoMax_pitch)
    time.sleep(2)
    print "俯仰云台收起！"
    tank.pwm.setPWM(tank.servoPitchNum, 0, tank.servoMid_pitch)
    print "俯仰云台部分结束！"
    print "="*40# 分割线
    print "偏航云台部分开始！"
    time.sleep(2)
    print "偏航云台展开！"
    tank.pwm.setPWM(tank.servoYawNum, 0, tank.servoMid_yaw)
    time.sleep(2)
    print "偏航云台最大仰角！"
    tank.pwm.setPWM(tank.servoYawNum, 0, tank.servoMax_yaw)
    time.sleep(2)
    print "偏航云台收起！"
    tank.pwm.setPWM(tank.servoYawNum, 0, tank.servoMid_yaw)
    print "偏航云台部分结束！"

    print "测试坦克车体————云台部分结束！"



if __name__ == "__main__":
    testTankRun()
    testTankLight()
    testTankPlatform()
