#!/usr/bin/python
# -*- coding:utf-8 -*-

from .HAT.Raspi_PWM_Servo_Driver import PWM

############################
# 用于控制坦克云台部分功能
############################
"""用于控制坦克云台部分"""


class Turret():
    # Initialise the PWM device using the default address
    # bmp = PWM(0x40, debug=True)
    pwm = PWM(0x6F)
    pwm.setPWMFreq(60)  # Set frequency to 60 Hz

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

    def ServoUpdate(channel, pulse):
        self.pwm.setPWM(channel, 0, pulse)

    # 俯仰 0-180 对应220到630
    def pitch(self, angle):
        if (angle <= 0):
            angle = 0
        elif (angle >= 180):
            angle = 180
        else:
            angle = angle

        #  求出每度角度对应的脉冲
        perAnglePulse = (self.servoMax_pitch - self.servoMin_pitch) / 180
        #  采用四舍五入的方式得到角度对应需要发送的脉冲宽度
        sendPulse = self.servoMin_pitch + round(angle * perAnglePulse)
        #  发送脉冲
        self.ServoUpdate(self.servoPitchNum, sendPulse)

    # 偏航
    def yaw(self, angle):
        if angle <= 0:
            angle = 0
        elif angle >= 180:
            angle = 180
        else:
            angle = angle
        #  求出每度角度对应的脉冲
        perAnglePulse = (self.servoMax_yaw - self.servoMin_yaw) / 180
        #  采用四舍五入的方式得到角度对应需要发送的脉冲宽度
        sendPulse = self.servoMin_yaw + round(angle * perAnglePulse)
        #  发送脉冲
        self.ServoUpdate(self.servoPitchNum, sendPulse)

    # 云台进入收藏状态
    def turret_off(self):
        self.pitch(0)
        self.yaw(90)
